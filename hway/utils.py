from .models import CodingQuestion, FacebookUser, CodingResult, BotUser, CourseSegment

import json, requests
import os
from binascii import hexlify

numbers = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

def validate_code(source, question_id, language_used, facebook_id):

    try:
        current_question=CodingQuestion.objects.get(pk=question_id)

    except:
        current_question=None


    if current_question:
        score=get_score(current_question.difficulty_level)
        total_score=0

        solution = current_question.solution
        test_cases = current_question.input
        solution_language=int(current_question.solution_language)
        possible_total=len(json.loads(test_cases))*score

        solution_data = {
            'api_key': 'hackerrank|394048-2076|cbdd81cef0663eb85cd43e24355f42b1efa2e2a8',
            'source': solution,
            'lang': solution_language,
            'testcases': test_cases,
            'format': 'JSON'
        }
        user_data = {
            'api_key': 'hackerrank|394048-2076|cbdd81cef0663eb85cd43e24355f42b1efa2e2a8',
            'source': source,
            'lang': language_used,
            'testcases': test_cases,
            'format': 'JSON'
        }

        url = 'http://api.hackerrank.com/checker/submission.json'

        user_output = requests.post(url, data=user_data).json()
        solution_output = requests.post(url, data=solution_data).json()

        print(user_output)
        print(solution_output)

        try:
            user_messages = user_output['result']['message']
        except:
            user_messages=None
        try:
            user_stderr = user_output['result']['stderr']
        except:
            user_stderr=None

        try:
            user_stdout = user_output['result']['stdout']
        except:
            user_stdout=None

        try:
            solution_stdout = solution_output['result']['stdout']
        except:
            solution_stdout=None

        print(solution_stdout)

        if user_stdout == None:
            compile_message = user_output['result']['compilemessage']
            create_score(facebook_id=facebook_id, testcase_index=0, question_id=question_id, source_code=source, error=compile_message, possible_total=possible_total)
            return {
                'compile_message': compile_message
            }

        else:
            for l in range(len(user_stderr)):
                if user_messages[l] != 'Success':
                    error = user_stderr[l]
                    create_score(facebook_id=facebook_id, testcase_index=l, question_id=question_id, source_code=source,score=total_score, error=error, possible_total=possible_total)
                    return {
                        'failed test': test_cases[l],
                        'std_error': user_stderr[l]
                    }

                else:
                    total_score=total_score+score

        zipped_output = [list(k) for k in zip(user_stdout, solution_stdout)]

        total_score=0
        for l in range(len(zipped_output)):
            if zipped_output[l][0] != zipped_output[l][1]:
                error='Found: '+ user_stdout[l]+ '\n'+ 'Expected: '+ solution_stdout[l]
                create_score(facebook_id=facebook_id, question_id=question_id, testcase_index=l, source_code=source, error=error, score=total_score, possible_total=possible_total)
                return {
                    'failed test': json.loads(test_cases)[l],
                    'found': user_stdout[l],
                    'expected': solution_stdout[l]
                }
            else:
                total_score=total_score+score

        create_score(facebook_id=facebook_id, question_id=question_id, testcase_index=len(json.loads(test_cases)), source_code=source, score=total_score, possible_total=possible_total)
        return {
            'success': 'Passed all test cases'
        }
    else:
        return {
            'error': 'We could not get the requested question'
        }


def create_score(facebook_id, question_id,testcase_index, source_code, error=None, score=0, possible_total=0):
    try:
        current_result=CodingResult.objects.get(coder_facebook_id=facebook_id, question_solved_id=question_id)
        current_result.last_testcase_passed_index=testcase_index
        current_result.coder_source_code=source_code
        current_result.error=error
        scores=json.loads(current_result.scores)
        scores.append(score)
        current_result.scores=json.dumps(scores)
        current_result.possible_total=current_result.possible_total+possible_total
        current_result.save()
    except:
        scores=[score]
        current_result=CodingResult(
            coder_facebook_id=facebook_id,
            question_solved_id=question_id,
            last_testcase_passed_index=testcase_index,
            coder_source_code=source_code,
            error=error,
            scores=json.dumps(scores),
            possible_total=possible_total
        )
        current_result.save()


def get_score(level):
    score=0
    if level == 'simple':
        score = 1
    elif level == 'intermediate':
        score = 2
    elif level == 'difficult':
        score = 3

    return score


def get_individual_score(facebook_id, messenger_id):
    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)

    if current_bot_user.possible_total>0:
        quiz_score = (sum(json.loads(current_bot_user.scores)) / current_bot_user.possible_total) * 100
        quiz_score = round(quiz_score, 2)
    else:
        quiz_score=0

    current_results = CodingResult.objects.filter(coder_facebook_id=facebook_id)

    all_scores = []
    possible_total = 0
    for current_result in current_results:
        all_scores = all_scores + json.loads(current_result.scores)
        possible_total = possible_total + current_result.possible_total

    if possible_total >0:
        challenge_score = (sum(all_scores) / possible_total) * 100
        challenge_score = round(challenge_score, 2)
    else:
        challenge_score=0

    overall_score = ((sum(json.loads(current_bot_user.scores)) + sum(all_scores)) / (
    current_bot_user.possible_total + possible_total)) * 100
    overall_score = round(overall_score, 2)

    return {
        'quiz_score': quiz_score,
        'challenge_score': challenge_score,
        'overall_score': overall_score
    }


def generate_api_key(length):
    random_byte=os.urandom(length)
    api_key=hexlify(random_byte).decode()
    return api_key

def get_number_emoji(number):
    number = str(number)
    res = ''
    for l in number:
        res += numbers[int(l)]

    return res


#validates code coming from the coding ground
def validate_ground_code(source, language_used, testcases):


    dummy_test_cases=['1']

    user_data = {
        'api_key': 'hackerrank|394048-2076|cbdd81cef0663eb85cd43e24355f42b1efa2e2a8',
        'source': source,
        'lang': language_used,
        'testcases':testcases,
        'format': 'JSON'
    }

    url = 'http://api.hackerrank.com/checker/submission.json'

    user_output = requests.post(url, data=user_data).json()

    print(user_output)

    try:
        user_messages = user_output['result']['message']
    except:
        user_messages=None
    try:
        user_stderr = user_output['result']['stderr']
    except:
        user_stderr=None

    try:
        user_stdout = user_output['result']['stdout']
    except:
        user_stdout=None


    if user_stdout == None:
        try:
            compile_message = user_output['result']['compilemessage']
        except:
            compile_message=None
        return {
            'success': False,
            'compile_message': compile_message
        }

    else:
        if user_stderr[0]==False:
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
        
    
    



