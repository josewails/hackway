import json
import requests
from django.core import exceptions
from django.conf import settings

from messenger.utils import (
    get_score
)

from hway.models import (
    CodingQuestion,
    CodingResult,
    BotUser
)

def validate_code(source, question_id, language_used, facebook_id):
    """

    :param source:
        this is the source code received from the application
    :param question_id:
        this the id of the question for which the above source  code is answer.
    :param language_used:
        the language used for the source code above
    :param facebook_id:  e
        the facebook id of the user who sent the source code
    :return:
    """

    try:
        current_question = CodingQuestion.objects.get(pk=question_id)

    except exceptions.ObjectDoesNotExist:
        current_question = None

    if current_question:
        score = get_score(current_question.difficulty_level)
        total_score = 0

        solution = current_question.solution
        test_cases = current_question.input
        solution_language = int(current_question.solution_language)
        possible_total = len(json.loads(test_cases)) * score

        solution_data = {
            'api_key': settings.HACKERRANK_API_KEY,
            'source': solution,
            'lang': solution_language,
            'testcases': test_cases,
            'format': 'JSON'
        }

        user_data = {
            'api_key': settings.HACKERRANK_API_KEY,
            'source': source,
            'lang': language_used,
            'testcases': test_cases,
            'format': 'JSON'
        }

        url = 'http://api.hackerrank.com/checker/submission.json'

        user_output = requests.post(url, data=user_data).json()
        solution_output = requests.post(url, data=solution_data).json()

        try:
            user_messages = user_output['result']['message']
        except KeyError:
            user_messages = None
        try:
            user_stderr = user_output['result']['stderr']
        except KeyError:
            user_stderr = None

        try:
            user_stdout = user_output['result']['stdout']
        except KeyError:
            user_stdout = None

        try:
            solution_stdout = solution_output['result']['stdout']
        except KeyError:
            solution_stdout = None

        # If the code did not compile successfully,
        # Get the error message and return it

        if not user_stdout:
            compile_message = user_output['result']['compilemessage']
            create_score(
                facebook_id=facebook_id, testcase_index=0, question_id=question_id, source_code=source,
                error=compile_message, possible_total=possible_total
            )
            return {
                'compile_message': compile_message
            }


        # If the code compiled successfully,
        # I go through all the results from the api
        # Checking if any of them of failed and if yes,
        # I return the failed test.
        # Otherwise I increase the current score with the value of score

        else:
            for l in range(len(user_stderr)):
                if user_messages[l] != 'Success':
                    error = user_stderr[l]
                    create_score(
                        facebook_id=facebook_id, testcase_index=l, question_id=question_id, source_code=source,
                        score=total_score, error=error, possible_total=possible_total
                    )
                    return {
                        'failed test': test_cases[l],
                        'std_error': user_stderr[l]
                    }

                else:
                    total_score = total_score + score

        # Zip the user output and the expected output into one list so that I can loop over them together.

        zipped_output = [list(k) for k in zip(user_stdout, solution_stdout)]

        # Make the value of total score = 1
        total_score = 0

        # We loop through the user output and the expected output.
        # We then check for an instance where they differ.
        # If we find such an instance, then this is a wrong answer.
        # We will return with the failed test
        # Otherwise, the user has passed all tests and they get a success message

        for l in range(len(zipped_output)):
            if zipped_output[l][0] != zipped_output[l][1]:
                error = 'Found: ' + user_stdout[l] + '\n' + 'Expected: ' + solution_stdout[l]
                create_score(
                    facebook_id=facebook_id, question_id=question_id, testcase_index=l, source_code=source, error=error,
                    score=total_score, possible_total=possible_total
                )
                return {
                    'failed test': json.loads(test_cases)[l],
                    'found': user_stdout[l],
                    'expected': solution_stdout[l]
                }
            else:
                total_score = total_score + score

        create_score(
            facebook_id=facebook_id, question_id=question_id, testcase_index=len(json.loads(test_cases)),
            source_code=source, score=total_score, possible_total=possible_total
        )

        return {
            'success': 'Passed all test cases'
        }

    else:
        return {
            'error': 'We could not get the requested question'
        }

def create_score(facebook_id, question_id, testcase_index, source_code, error=None, score=0, possible_total=0):
    """

    :param facebook_id:
        The facebook id of the user for whom we are going to create a score for.
    :param question_id:
        The  question id for which we are going to create a score for.
    :param testcase_index:
        The index of the test case.
    :param source_code:
        The source code which had been submitted.
    :param error:
        An error if any.
    :param score:
        Score obtained by the user
    :param possible_total:
        The possible total score
    :return:

    """
    try:
        current_result = CodingResult.objects.get(coder_facebook_id=facebook_id, question_solved_id=question_id)

    except exceptions.ObjectDoesNotExist:
        scores = [score]
        current_result = CodingResult(
            coder_facebook_id=facebook_id,
            question_solved_id=question_id,
            last_testcase_passed_index=testcase_index,
            coder_source_code=source_code,
            error=error,
            scores=json.dumps(scores),
            possible_total=possible_total
        )
        current_result.save()

    else:
        current_result.last_testcase_passed_index = testcase_index
        current_result.coder_source_code = source_code
        current_result.error = error

        scores = json.loads(current_result.scores)
        scores.append(score)
        current_result.scores = json.dumps(scores)
        current_result.possible_total = current_result.possible_total + possible_total
        current_result.save()

def get_individual_score(facebook_id, messenger_id):
    """

    :param facebook_id: the facebook id of the user
    :param messenger_id: the messenger id of the user
    :return:
          a dict object containing the following data of the specific user:
          1. Their average score in the quizzes
          2.Their average score in the programming challenges
          3.Their overall score
    """

    # Get the bot_user associated with the given messenger id

    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)

    # Get their score in the quizzes
    # The score of the quizes is saved within the BotUser Model

    if current_bot_user.possible_total > 0:
        quiz_score = (sum(json.loads(current_bot_user.scores)) / current_bot_user.possible_total) * 100
        quiz_score = round(quiz_score, 2)
    else:
        quiz_score = 0

    # Get their results for the programming questions. They are identified using the unique facebook id

    current_results = CodingResult.objects.filter(coder_facebook_id=facebook_id)

    all_scores = []
    possible_total = 0

    # Calculate their average score in the quizzes

    for current_result in current_results:
        all_scores = all_scores + json.loads(current_result.scores)
        possible_total = possible_total + current_result.possible_total

    if possible_total > 0:
        challenge_score = (sum(all_scores) / possible_total) * 100
        challenge_score = round(challenge_score, 2)
    else:
        challenge_score = 0

    # Calculate their overall average score
    overall_score = ((sum(json.loads(current_bot_user.scores)) + sum(all_scores)) /
                     (current_bot_user.possible_total + possible_total)) * 100
    overall_score = round(overall_score, 2)

    return {
        'quiz_score': quiz_score,
        'challenge_score': challenge_score,
        'overall_score': overall_score
    }


def validate_ground_code(source, language_used, testcases):
    user_data = {
        'api_key': settings.HACKERRANK_API_KEY,
        'source': source,
        'lang': language_used,
        'testcases': testcases,
        'format': 'JSON'
    }

    url = 'http://api.hackerrank.com/checker/submission.json'

    user_output = requests.post(url, data=user_data).json()

    try:
        user_messages = user_output['result']['message']
    except KeyError:
        user_messages = None

    try:
        user_stderr = user_output['result']['stderr']
    except KeyError:
        user_stderr = None

    try:
        user_stdout = user_output['result']['stdout']
    except KeyError:
        user_stdout = None

    # Check whether there is any compile error message
    # If there is one, We just return the error message,
    # Else, We return  a success message

    if not user_stdout:
        try:
            compile_message = user_output['result']['compilemessage']
        except KeyError:
            compile_message = None

        return {
            'success': False,
            'compile_message': compile_message
        }

    else:
        if not user_stderr[0]:
            return {
                'success': True,
                'result': user_stdout[0]
            }
        else:
            return {
                'success': False,
                'message': user_messages[0],
                'error': user_stderr[0]
            }