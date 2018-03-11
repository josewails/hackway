from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from pymessenger.bot import Bot
from .models import(
    BotUser,
    CodingResult,
    CodingQuestion,
    ProgrammingQuestion,
    ProgrammingQuestionAnswer,
    FacebookUser,
    ProgrammingCategory,
    CourseSegment
)

import json
import requests
import urllib.parse
import random
import logging
from .utils import (
    get_score,
    share_with_template,
    text_quick_reply,
    element,
    plain_element,
    postback_button,
    share_button,
    web_button
)

# online
# page_access_token='EAAB9qLtZBAGoBALIZAUXOsrwZAQZAdnApZADJZCnwtkRdrLFr8ZBn
# QiNM7KhNGocTHA15qnKwzgbplmzWMPgR5wbW7lrxd5Qr6NXdbebdOUfSBBBlRxoYIupXKw5vAeqV4k1W4Dkcr5QMZB4q3fi3IobFEbrJaZAoUadFVsmzptRPYZBSDHBg0aPmA'

# local
page_access_token = 'EAAB9qLtZBAGoBAO5QtdugUWTyKkzLMCkNzrrvZB5h' + \
                    'qtuuPyNlagIuNqLHWUW8vDltKFu8BWsnIKXP245yqDZB' + \
                    'xnqN5rM0YrxrwWzuhpo1fFVJhCC6d5sYbp5OboegQQUe' + \
                    'jEM4v0ZBLfdgA9p5nJYlfc3Qg0rGTJ3fhPCk1YEfgZDZD'

messenger_bot = Bot(page_access_token)
base_url = 'https://hackway.surge.sh'
bot_url = 'https://m.me/2073931602829622'
logger = logging.getLogger(__name__)

@csrf_exempt
def webhook(request):
    # this one is used to authenticate the webhook on messenger
    if request.method == 'GET':
        if 'hub.mode' in request.GET and 'hub.verify_token' in request.GET:
            if request.GET['hub.mode'] == 'subscribe' and request.GET['hub.verify_token'] == 'hacking_the_way':
                return HttpResponse(request.GET['hub.challenge'])
            else:
                return HttpResponse("Wrong verification code")
        else:
            return HttpResponse("Bi :p")

    elif request.method == 'POST':

        print("I am here")
        # decodes the request and then converts it into json format
        request_body = request.body.decode('utf-8')
        req = json.loads(request_body)
        recipient_id = req['entry'][0]['messaging'][0]['sender']['id']

        # The following block of try-except blocks just checks for what type of message we are receiving
        try:
            BotUser.objects.get(messenger_id=recipient_id)
        except ObjectDoesNotExist:
            create_new_bot_user(recipient_id=recipient_id)
            logger.info("Created a new bot user")
        try:
            post_back = req['entry'][0]['messaging'][0]['postback']
        except KeyError:
            post_back = None
            logger.warning("postback set to None")

        try:
            quick_reply_message = req['entry'][0]['messaging'][0]['message']['quick_reply']
        except KeyError:
            quick_reply_message = None
            logger.warning("Quick reply message set to None")

        try:
            text_message = req['entry'][0]['messaging'][0]['message']['text']
        except KeyError:
            text_message = None
            logger.warning("text  message set to None")

        try:
            referral = req['entry'][0]['messaging'][0]['referral']
        except KeyError:
            referral = None
            logger.info("set referral to None")

        try:
            get_started_referral = req['entry'][0]['messaging'][0]['postback']['referral']
        except KeyError as err:
            get_started_referral = None
            logger.info('Set get_started_referral to None')


        if text_message and not quick_reply_message:
            handle_text_message(recipient_id, text_message=text_message)

        elif quick_reply_message:
            handle_quick_reply(recipient_id, quick_reply_message)

        elif post_back:
            handle_post_back(recipient_id=recipient_id, post_back=post_back, get_started_referral=get_started_referral)

        elif referral:
            handle_referral(recipient_id, referral)

    HttpResponse.status_code = 200
    return HttpResponse('')


def handle_post_back(recipient_id, post_back, get_started_referral=None):
    payload = post_back['payload']

    if payload == 'get_started':
        handle_get_started(recipient_id=recipient_id)

        if get_started_referral:
            print('get started referral')
            handle_referral(recipient_id, get_started_referral)

    elif payload == 'options':
        handle_options_payload(recipient_id=recipient_id)
    elif payload == 'programming_questions':
        handle_programming_questions_payload(recipient_id=recipient_id)

    elif payload == 'programming_multiple_answer':
        handle_programming_multiple_answer_payload(recipient_id=recipient_id)

    elif 'language_code' in payload:
        handle_language_code_postback(recipient_id=recipient_id, payload=payload)

    elif payload == 'generate_quiz':
        handle_generate_quiz_payload(messenger_id=recipient_id)

    elif payload == 'how_to_challenge':
        handle_how_to_challenge_payload(messenger_id=recipient_id)

    elif payload == 'main_menu':
        send_menu(messenger_id=recipient_id)


def handle_quick_reply(recipient_id, quick_reply_message):
    payload = quick_reply_message['payload']

    if payload == 'programming_questions':
        handle_programming_questions_payload(recipient_id=recipient_id)

    elif payload == 'programming_multiple_answer':
        handle_programming_multiple_answer_payload(recipient_id=recipient_id)

    elif 'language_code' in payload:
        payload = json.loads(payload)
        handle_language_code_postback(recipient_id=recipient_id, payload=payload)

    elif 'category_id' in payload:
        payload = json.loads(payload)
        handle_category_id_payload(recipient_id=recipient_id, payload=payload)

    elif 'difficulty_level' in payload:
        payload = json.loads(payload)
        handle_difficulty_level_payload(recipient_id=recipient_id, payload=payload)

    elif 'answer_id' in payload:
        payload = json.loads(payload)
        handle_answer_id_payload(recipient_id=recipient_id, payload=payload)

    elif payload == 'main_menu':
        send_menu(messenger_id=recipient_id)

    elif payload == 'quiz_solve_more':
        send_question(messenger_id=recipient_id, state={'text_message': ''})

    elif payload == 'question_solve_more':
        handle_programming_questions_payload(recipient_id=recipient_id)


def handle_how_to_challenge_payload(messenger_id):

    procedure = "     How to ⁉️\n" \
              "❇️ Solve a Quiz or Programming Question\n\n" \
              "❇️ After getting your results, Click on Share\n\n" \
              "❇️ Send the Quiz/Question to  a friend\n\n" \
              "❇️ Your friend receives the same Quiz/Question\n\n" \
              "❇️ Get notified when they solve it\n"

    messenger_bot.send_action(recipient_id=messenger_id, action='typing_on')
    messenger_bot.send_text_message(recipient_id=messenger_id, message=procedure)

    message = "🗣️ Ready to challenge someone? 💪 Choose an option Below 👇"
    btn1 = postback_button(
        title='🔘Quiz ✍️ ',
        payload='programming_multiple_answer',
    )

    btn2 = postback_button(
        title='🔘 Programming💻 ',
        payload='programming_questions'
    )

    messenger_bot.send_action(action='typing_on', recipient_id=messenger_id)
    messenger_bot.send_button_message(recipient_id=messenger_id, text=message, buttons=[btn1, btn2])


def unhung(recipient_id):
    messenger_bot.send_text_message(recipient_id=recipient_id, message='Unhunging You')


def handle_generate_quiz_payload(messenger_id):

    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    current_bot_user.generating_quiz = True
    quiz_results = json.loads(current_bot_user.generated_quiz_results)
    quiz_results['average_score'] = 0
    quiz_results['total_score'] = 0
    current_bot_user.generated_quiz_results = json.dumps(quiz_results)
    current_bot_user.save()

    # go through the normal loop of sending categories e.t.c
    handle_programming_multiple_answer_payload(messenger_id)


def handle_referral(messenger_id,referral):
    ref = referral['ref']
    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    if 'quiz_data' in ref:
        quiz_data = json.loads(ref)['quiz_data']

        json_data = json.loads(current_bot_user.json_store)
        json_data['language_code'] = quiz_data['language_code']
        json_data['difficulty_level'] = quiz_data['difficulty_level']

        challenger = BotUser.objects.get(messenger_id=quiz_data['challenger_id'])
        challenger.quiz_challenged = False
        challenger.save()

        current_bot_user.json_store = json.dumps(json_data)
        current_bot_user.quiz_challenged = True
        current_bot_user.quiz_data = json.dumps(quiz_data)
        current_bot_user.current_questions_ids = quiz_data['questions_done_ids']
        current_bot_user.questions_right = 0
        current_bot_user.questions_done = 0

        current_bot_user.save()

        send_question(current_bot_user.messenger_id, state={'text_message': ''})

    elif 'challenge_data' in ref:
        challenge_data = json.loads(ref)['challenge_data']
        challenger = BotUser.objects.get(messenger_id=challenge_data['challenger_id'])

        current_bot_user.question_challenged = True
        challenger.question_challenged = False

        current_bot_user.question_data = json.dumps(challenge_data)
        current_bot_user.save()
        challenger.save()

        question_id = challenge_data['question_id']
        current_question = CodingQuestion.objects.get(id=question_id)

        btn = messenger_extensions_button(
            title="Try it",
            url=base_url+'/all_coding_questions/'+str(current_question.id),
            messenger_extensions=True,
            height='Full'
        )

        el = plain_element(
            title="Question",
            subtitle=current_question.question,
            buttons=[btn]
        )

        messenger_bot.send_generic_message(recipient_id=messenger_id, elements=[el])

    elif 'generated_q_data' in ref:

        quiz_data = json.loads(ref)['generated_q_data']

        json_data = json.loads(current_bot_user.json_store)
        json_data['language_code'] = quiz_data['language_code']
        json_data['difficulty_level'] = quiz_data['difficulty_level']

        challenger = BotUser.objects.get(messenger_id=quiz_data['challenger_id'])
        challenger.generated_quiz_challenged = False
        challenger.save()

        current_bot_user.json_store = json.dumps(json_data)
        current_bot_user.generated_quiz_challenged = True
        current_bot_user.quiz_data = json.dumps(quiz_data)
        current_bot_user.current_questions_ids = quiz_data['questions_ids']
        current_bot_user.questions_right = 0
        current_bot_user.questions_done = 0

        current_bot_user.save()

        send_question(current_bot_user.messenger_id, state={'text_message': ''})

    elif 'segment_id' in ref:
        segment_id = json.loads(ref)['segment_id']
        send_code_segment_quiz(messenger_id=messenger_id, segment_id=segment_id)


def handle_options_payload(recipient_id):
    qr2 = text_quick_reply(
        title='Programming',
        payload='programming_questions'
    )

    qr1 = text_quick_reply(
        title='Multiple Answer',
        payload='programming_multiple_answer'
    )

    q3 = text_quick_reply(
        title='☱ Menu',
        payload='main_menu'
    )

    message = {
        'text': 'Choose the type of Question you would like to solve',
        'quick_replies': [qr1, qr2, q3]
    }

    messenger_bot.send_action(recipient_id=recipient_id, action='typing_on')
    messenger_bot.send_message(recipient_id=recipient_id, message=message)


def send_post_quiz_replies(messenger_id):
    q1 = text_quick_reply(
        title='☱ Menu',
        payload='main_menu'
    )

    q2 = text_quick_reply(
        title='✍️Solve More',
        payload='quiz_solve_more'
    )

    message = {
        'text': '👇',
        'quick_replies': [q1, q2]
    }

    messenger_bot.send_message(recipient_id=messenger_id, message=message)


def send_post_question_replies(messenger_id):
    emoji_choices = ['👨‍💻', '👩‍💻']
    q1 = text_quick_reply(
        title='☱ Menu',
        payload='main_menu'
    )

    q2 = text_quick_reply(
        title=random.choice(emoji_choices)+"More Questions",
        payload='question_solve_more'
    )

    message = {
        'text': '👇',
        'quick_replies': [q1, q2]
    }

    messenger_bot.send_message(recipient_id=messenger_id, message=message)


def handle_category_id_payload(recipient_id, payload):
    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    category_id = payload['category_id']

    json_data = json.loads(current_bot_user.json_store)
    json_data['category_id'] = category_id
    current_bot_user.json_store = json.dumps(json_data)
    current_bot_user.save()

    message = "Select your favourite programming language"
    messenger_bot.send_action(action='typing_on', recipient_id=recipient_id)
    messenger_bot.send_text_message(recipient_id=recipient_id, message=message)

    current_category = ProgrammingCategory.objects.get(id=category_id)
    programming_languages = current_category.programminglanguage_set.all()

    elements = []
    for programming_language in programming_languages:
        if programming_language.published:
            payload = {
               'language_code': programming_language.code
            }

            btn = postback_button(
                title=programming_language.name,
                payload=json.dumps(payload)
            )

            btns = [btn]

            # image_url = programming_language.logo.url
            image_url = 'https://www.python.org/static/opengraph-icon-200x200.png'
            current_element = plain_element(
                title=programming_language.name,
                image_url=image_url,
                buttons=btns
            )

            elements.append(current_element)

    messenger_bot.send_generic_message(recipient_id=recipient_id, elements=elements)


def handle_difficulty_level_payload(recipient_id, payload):

    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    difficulty_level = payload['difficulty_level']

    json_data = json.loads(current_bot_user.json_store)
    json_data['difficulty_level'] = difficulty_level

    current_bot_user.json_store = json.dumps(json_data)
    current_bot_user.save()

    if current_bot_user.generating_quiz:
        generate_quiz(messenger_id=recipient_id)
        current_bot_user.generating_quiz = False
        current_bot_user.save()

    else:
        send_question(messenger_id=recipient_id, state={'text_message': ''})


def handle_programming_multiple_answer_payload(recipient_id):

    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)

    # They are starting a new quiz. What if they left another one hanging? Avoid issues
    current_bot_user.questions_done = 0
    current_bot_user.questions_right = 0
    current_bot_user.current_questions_ids = json.dumps([])
    current_bot_user.challenged = False
    current_bot_user.quiz_challenged = False
    current_bot_user.question_challenged = False
    current_bot_user.solving_course_quiz = False
    current_bot_user.save()

    # Move on with the flow
    text = 'Choose one of the following categories'

    categories = ProgrammingCategory.objects.all()

    quick_replies = []

    for category in categories:
        payload = {
            'category_id': category.id
        }

        qr = text_quick_reply(
            title=category.name,
            payload=json.dumps(payload)
        )

        quick_replies.append(qr)

    message = {
        'text': text,
        'quick_replies': quick_replies
    }

    # send all the categories
    messenger_bot.send_action(action='typing_on', recipient_id=recipient_id)
    messenger_bot.send_message(recipient_id=recipient_id, message=message)


def handle_answer_id_payload(recipient_id, payload):
    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    ans_id = int(payload['answer_id'])
    current_question = ProgrammingQuestionAnswer.objects.get(id=ans_id).related_question
    qs_id = current_question.id

    state = check_answer(ans_id, qs_id)

    if state is True:
        current_bot_user.questions_right += 1
        current_bot_user.save()

        if current_question.difficulty_level == 'simple':
            current_bot_user.quiz_total += 1
            current_bot_user.save()

        elif current_question.difficulty_level == 'intermediate':
            current_bot_user.quiz_total += 3
            current_bot_user.save()

        elif current_question.difficulty_level == 'difficult':
            current_bot_user.quiz_total += 5
            current_bot_user.save()

        message = "☑️ You got it right 💪"

        if current_question.explanation:
            btn = messenger_extensions_button(
                title='👀 ️See Explanation',
                url=base_url+'/programming_question_explanation/'+str(current_question.id),
                messenger_extensions=True,
                height='compact'
            )

            btns = [btn]
            ret_state = {
                'button_message': message,
                'buttons': btns
            }
        else:
            ret_state = {
                'text_message': message
            }

        send_question(messenger_id=recipient_id, state=ret_state)

    else:
        message = "✖️ Wrong 😞 The Right Answer is " + state
        if current_question.explanation:
            btn = messenger_extensions_button(
                title='👀 ️See Explanation',
                url=base_url+'/programming_question_explanation/'+str(current_question.id),
                messenger_extensions=True,
                height='compact'
            )

            btns = [btn]
            ret_state = {
                'button_message': message,
                'buttons': btns
            }
        else:
            ret_state = {
                'text_message': message

            }

        send_question(messenger_id=recipient_id, state=ret_state)


def handle_programming_questions_payload(recipient_id):
    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    current_bot_user.questions_done = 0
    current_bot_user.questions_right = 0
    current_bot_user.save()

    b1 = messenger_extensions_button(
        title='Easy',
        url=base_url + '/all_coding_questions/difficulty_level/simple',
        messenger_extensions=True,
        height='full'
    )

    b2 = messenger_extensions_button(
        title='Intermediate',
        url=base_url + '/all_coding_questions/difficulty_level/intermediate',
        messenger_extensions=True,
        height='full'
    )

    b3 = messenger_extensions_button(
        title='Difficult',
        url=base_url + '/all_coding_questions/difficulty_level/difficult',
        messenger_extensions=True,
        height='full'
    )

    buttons = [b1, b2, b3]

    messenger_bot.send_action(recipient_id=recipient_id, action='typing_on')
    messenger_bot.send_button_message(recipient_id=recipient_id, buttons=buttons, text='Choose a difficulty level')


def handle_language_code_postback(recipient_id, payload):
    current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    payload = json.loads(payload)
    language_code = payload['language_code']

    json_data = json.loads(current_bot_user.json_store)
    json_data['language_code'] = language_code

    current_bot_user.json_store = json.dumps(json_data)
    current_bot_user.save()

    difficulty_levels = ['simple', 'intermediate', 'difficult']

    quick_replies = []

    for level in difficulty_levels:
        payload = {
            'difficulty_level': level
        }

        q = text_quick_reply(
            title=level,
            payload=json.dumps(payload)
        )

        quick_replies.append(q)

    text = 'Choose  one of the following difficulty levels'
    message = {
        'text': text,
        'quick_replies': quick_replies
    }

    messenger_bot.send_action(action='typing_on', recipient_id=recipient_id)
    messenger_bot.send_message(recipient_id=recipient_id, message=message)


def send_results(messenger_id, facebook_id, question_id):

    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    current_facebook_user = FacebookUser.objects.get(facebook_id=facebook_id)

    if not current_bot_user.facebook_user:
        current_bot_user.facebook_user = current_facebook_user
        current_bot_user.save()

    try :
        current_result = CodingResult.objects.get(coder_facebook_id=facebook_id, question_solved_id=question_id)
    except ObjectDoesNotExist as err:
        current_result = None
        logger.warning('Current result set to None')

    try:
        current_question = CodingQuestion.objects.get(id=question_id)
    except:
        current_question = None

    if current_result:

        if current_question:
            testcase_index = current_result.last_testcase_passed_index
            testcases = json.loads(current_question.input)

            scores = json.loads(current_result.scores)
            possible_score = len(testcases)*get_score(current_question.difficulty_level)
            score = round((scores[-1] / possible_score), 4) * 100

            if len(testcases)==testcase_index:

                data = {
                    'success': True,
                    'question': current_question.title,
                    'score': score
                }

            else:
                data = {
                    'success': False,
                    'question': current_question.title,
                    'testcase_failed': testcases[testcase_index],
                    'score': score
                }

        else:
            data = {
                'error': 'Looks like that coding problem does not exist'
            }

    else:
        data = {
            'error': 'we could not retrieve the requested resource'
        }


    if data:
        try_again_button = messenger_extensions_button(
            title='Try Again',
            url=base_url + '/all_coding_questions/' + str(question_id),
            messenger_extensions=True,
            height='full'
        )

        if 'error' in data:
            message = data['error']

            buttons = [try_again_button]
            messenger_bot.send_button_message(recipient_id=messenger_id, buttons=buttons, text=message)

        else:
            profile_data = get_profile_data(messenger_id=messenger_id)
            subtitle = profile_data['first_name']+ " "+ profile_data['last_name']+ " sent you a programming challenge"
            profile_picture_url = profile_data['profile_picture_url']
            payload = {
                'challenge_data': {
                    'challenger_id': current_bot_user.messenger_id,
                    'question_id': current_question.id,
                    'challenger_score': data['score']
                }
            }

            share_url = bot_url+"?ref="+urllib.parse.quote(json.dumps(payload))
            btn = web_button(
                title='👀 ️See Challenge',
                url=share_url
            )
            share_element = plain_element(
                title=current_question.title,
                subtitle=subtitle,
                image_url=profile_picture_url,
                buttons=[btn]
            )

            share_btn = share_with_template([share_element])

            if data['success'] == True:
                send_results_when_success(facebook_id=facebook_id, messenger_id=messenger_id, question_id=question_id, data=data, share_btn=share_btn)

            else:
                send_results_when_not_success(facebook_id=facebook_id, messenger_id=messenger_id, question_id=question_id,data=data, share_btn=share_btn)

    else:
        message = 'we experienced a problem trying to get your results :('
        btn = messenger_extensions_button(
            title='Try Again',
            url=base_url+'/all_coding_questions/' + str(question_id),
            messenger_extensions='True',
            height='full'
        )

        buttons = [btn]
        messenger_bot.send_button_message(recipient_id=messenger_id, buttons=buttons, text=message)

    send_post_question_replies(messenger_id=messenger_id)

def send_results_when_not_success(facebook_id, messenger_id, data, question_id, share_btn):
    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    challenger_id = None

    try_again_button = messenger_extensions_button(
        title='Try Again',
        url=base_url + '/all_coding_questions/' + str(question_id),
        messenger_extensions=True,
        height='full'
    )

    f1 = plain_element(
        title=data['question'],
        subtitle='Wanna challenger a friend with this Question? Click share ⬇️',
        buttons=[share_btn]
    )

    f2_btn = messenger_extensions_button(
        title='Get Help',
        url=base_url + '/question_share/' + str(question_id),
        messenger_extensions=True,
        height='compact'
    )

    if current_bot_user.question_challenged:
        question_data = json.loads(current_bot_user.question_data)
        challenger_id = question_data['challenger_id']
        challenger_score = str(question_data['challenger_score'])

        challenger_details = get_profile_data(challenger_id)
        challenged_details = get_profile_data(messenger_id)

        title = "Scores"
        subtitle = challenged_details['first_name'] + " " + challenged_details['last_name'] + " : " + str(
            data['score']) + "\n" \
                   + challenger_details['first_name'] + " " + challenger_details[
                       'last_name'] + " : " + challenger_score

        f2 = plain_element(
            title=title,
            subtitle=subtitle
        )

    else:
        f2_btns = [f2_btn]

        f2 = plain_element(
            title='Status',
            subtitle='Failed',
            buttons=f2_btns
        )

    f3_btn = messenger_extensions_button(
        title='Full Results',
        url=base_url + '/result/' + facebook_id + "/" + str(question_id),
        messenger_extensions=True,
        height='full'
    )

    s3_btns = [f3_btn]

    f3 = plain_element(
        title='Message',
        subtitle='Your code failed for this test case: ' + data['testcase_failed'],
        buttons=s3_btns
    )

    f4 = plain_element(
        title='Your Score in %:',
        subtitle=str(data['score'])
    )

    buttons = [try_again_button]
    elements = [f1, f2, f3, f4]

    if current_bot_user.question_challenged:
        current_bot_user.question_challenged = False
        current_bot_user.question_data = None
        current_bot_user.save()
        messenger_bot.send_plainlist_message(recipient_id=messenger_id, elements=elements, buttons=buttons)
        messenger_bot.send_text_message(recipient_id=challenger_id,
                                        message='Here are the results for a challenge you shared :)')
        messenger_bot.send_plainlist_message(recipient_id=challenger_id, elements=elements, buttons=buttons)

    else:
        messenger_bot.send_plainlist_message(recipient_id=messenger_id, elements=elements, buttons=buttons)


def send_results_when_success(data, messenger_id, facebook_id, question_id, share_btn):
    challenger_id = None
    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    share_btn = share_button()

    s1 = plain_element(
        title=data['question'],
        subtitle='Wanna challenger a friend with this Question? Click share ⬇️',
        buttons=[share_btn]
    )

    s2_btn = messenger_extensions_button(
        title='Share',
        url=base_url + '/result_share/' + str(facebook_id) + '/' + str(question_id),
        messenger_extensions=True,
        height='compact'
    )

    try_again_button = messenger_extensions_button(
        title='Try Again',
        url=base_url + '/all_coding_questions/' + str(question_id),
        messenger_extensions=True,
        height='full'
    )

    if current_bot_user.question_challenged:
        question_data = json.loads(current_bot_user.question_data)
        challenger_id = question_data['challenger_id']
        challenger_score = str(question_data['challenger_score'])

        challenger_details = get_profile_data(challenger_id)
        challenged_details = get_profile_data(messenger_id)

        title = "Challenge Scores"
        subtitle = challenged_details['first_name'] + " " + challenged_details['last_name'] + \
                   " : " + str(data['score']) + "\n" + \
                   + challenger_details['first_name'] + \
                   challenger_details['last_name'] + " : " + challenger_score

        s2 = plain_element(
            title=title,
            subtitle=subtitle
        )

    else:
        s2_btns = [s2_btn]

        s2 = plain_element(
            title='Status',
            subtitle='Success',
            buttons=s2_btns
        )

    s3_btn = messenger_extensions_button(
        title='Full Results',
        url=base_url + '/result/' + facebook_id + "/" + str(question_id),
        messenger_extensions=True,
        height='full'
    )

    s3_btns = [s3_btn]

    s3 = plain_element(
        title='Message',
        subtitle='you passed all test_cases',
        buttons=s3_btns
    )

    s4 = plain_element(
        title='Your Score in %',
        subtitle=str(data['score'])
    )

    buttons = [try_again_button]
    elements = [s1, s2, s3, s4]

    if current_bot_user.question_challenged:
        current_bot_user.question_challenged = False
        current_bot_user.question_data = None
        current_bot_user.save()
        messenger_bot.send_plainlist_message(recipient_id=messenger_id, elements=elements, buttons=buttons)
        messenger_bot.send_text_message(recipient_id=challenger_id,
                                        message='Here are the results for a challenge you shared :)')
        messenger_bot.send_plainlist_message(recipient_id=challenger_id, elements=elements, buttons=buttons)

    else:
        messenger_bot.send_plainlist_message(recipient_id=messenger_id, elements=elements, buttons=buttons)


@csrf_exempt
def send_code_results(request):
    if request.method == 'POST':
        try:
            fb_id = request.POST['facebook_id']
        except:
            fb_id = None

        try:
            q_id = request.POST['question_id']
        except:
            q_id = None

        try:
            m_id = request.POST['messenger_id']
        except:
            m_id = None

        if fb_id and q_id and m_id:
            send_results(messenger_id=m_id, facebook_id=fb_id, question_id=q_id)

        else:

            message='We experience a problem retrieving your results'

            btn = messenger_extensions_button(
                title='Try Again',
                url=base_url+'/all_coding_questions/' + str(q_id),
                messenger_extensions=True,
                height='full'
            )

            buttons = [btn]
            messenger_bot.send_button_message(recipient_id=m_id, buttons=buttons, text=message)
    else:
        # handle error for other methods
        data = {
            'error': 'that method is not allowed'
        }

        return JsonResponse(data)

    return HttpResponse('Hello there')


def handle_get_started(recipient_id):
    try:
        current_bot_user = BotUser.objects.get(messenger_id=recipient_id)
    except:
        current_bot_user = create_new_bot_user(recipient_id=recipient_id)

    if current_bot_user:
        profile_details = json.loads(current_bot_user.profile_details)
        try:
            name = profile_details['first_name']
        except:
            name = profile_details['last_name']


        subtitle = ("Let's 👀 what I have for you, Tap 'Options' below 👇 ")

        welcome_buttons = []

        welcome_button = postback_button(
            title='Options',
            payload='options'
        )

        welcome_buttons.append(welcome_button)

        love_emoji = '❤️'
        messenger_bot.send_text_message(recipient_id=recipient_id, message=love_emoji)

        if name:
            welcome_message="Hi " +name +",I am a bot that helps you solve programming challenges :)"
        else:
            welcome_message='Hi, I am a bot that helps solve programming challenges :)'

        welcome_element = element(
            title= welcome_message,
            subtitle=subtitle,
            image_url=None,
            buttons=welcome_buttons
        )

        welcome_elements = [welcome_element]

        messenger_bot.send_action(recipient_id=recipient_id, action="typing_on")
        messenger_bot.send_generic_message(recipient_id=recipient_id, elements=welcome_elements)


def handle_text_message(recipient_id, text_message):
    messenger_bot.send_text_message(recipient_id=recipient_id, message=text_message)


def send_menu(messenger_id):
    pc_button = postback_button(
        title='⌨️ Programming',
        payload='programming_questions'
    )

    mq_button = postback_button(
        '✍️  Multiple Answer',
        payload='programming_multiple_answer'
    )

    solve_buttons = [pc_button, mq_button]

    el1 = plain_element(
        title='Solve',
        subtitle='Improve your skill by solving Programming Challenges or Multiple Choice Answers',
        buttons=solve_buttons
    )

    mp_button = messenger_extensions_button(
        title='Your Progress',
        url=base_url+'/individual_ranking',
        messenger_extensions=True,
        height='full'
    )

    fr_button = messenger_extensions_button(
        title='Full Ranking',
        url=base_url + '/full_ranking',
        messenger_extensions=True,
        height='full'
    )

    ranking_buttons = [mp_button, fr_button]


    el2 = plain_element(
        title='Ranking',
        subtitle='👀 how you rank among other developers',
        buttons=ranking_buttons
    )

    gq_button = postback_button(
        title="Generate",
        payload='generate_quiz'
    )

    el3 = plain_element(
        title='Generate a Quiz',
        subtitle='➡️ Generate a Quiz, Send to a Group\n'
                 '➡️Get notification when anybody solves it',
        buttons=[gq_button]
    )

    cg_button = web_button(
        title='Code Ground',
        url=base_url+'/coding_ground'
    )

    el4 = plain_element(
        title='👩‍💻  👨‍💻 Coding Ground',
        subtitle="You can write and compile code quicky with HackWay's code ground 🕶️",
        buttons=[cg_button]
    )

    c_button = postback_button(
        title='👀 How',
        payload='how_to_challenge'
    )

    el5 = plain_element(
        title=' 💪 Challenge Friends',
        subtitle='Learn how you can challenge friends below ⬇️',
        buttons=[c_button]
    )

    elements = [el1,el3, el4, el5, el2]

    messenger_bot.send_generic_message(recipient_id=messenger_id, elements=elements)


def messenger_extensions_button(title, url, messenger_extensions, height):
    button={
        'type': 'web_url',
        'title': title,
        'url': url,
        'messenger_extensions': messenger_extensions,
        'webview_height_ratio': height
    }

    return button


def create_new_bot_user(recipient_id):

    """
    -> Get the details of the facebook user whose messenger id corresponds to the current recipient_id

    :param recipient_id:
    :return:
    """


    user_details = get_facebook_details(recipient_id)
    current_bot_user = BotUser(messenger_id=recipient_id, profile_details=json.dumps(user_details))
    current_bot_user.save()


def get_facebook_details(facebook_id):
    """
     ->Gets the user details specified in *fields* of the user with the given facebook id and returns them

    :param user_id:
    :return:
    """
    fields = 'first_name,last_name,gender,locale,timezone,profile_pic'

    fb_url = 'https://graph.facebook.com/v2.6/' + facebook_id

    my_data = {
        'fields': fields,
        'access_token': page_access_token
    }

    r = requests.get(url=fb_url, params=my_data)

    profile_data = r.json()
    print(profile_data)
    return profile_data


def get_questions_data(current_bot_user):
    json_data = json.loads(current_bot_user.json_store)
    try :
        language_code = json_data['language_code']
    except KeyError:
        language_code=None
        logger.info("Language code set to None")

    try:
        difficulty = json_data['difficulty_level']
    except KeyError:
        difficulty=None
        logger.info("difficulty set to None")

    if language_code and difficulty:
        questions = ProgrammingQuestion.objects.filter(language__code=language_code, difficulty_level=difficulty)
        questions_ids = [question.id for question in questions]

        if len(questions_ids)>10:
            questions_ids = random.sample(questions_ids, 10)

    else:
        questions = []
        questions_ids = []

    return [questions, questions_ids, language_code, difficulty]

def send_question(messenger_id, state):
    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    questions_done = current_bot_user.questions_done
    
    current_questions_ids = json.loads(current_bot_user.current_questions_ids)

    if len(current_questions_ids) == 0:
        questions_data = get_questions_data(current_bot_user)
        questions, questions_ids,language_code, difficulty = questions_data[0], questions_data[1], questions_data[2], questions_data[3]

        if len(questions) == 0:
            message = "We don't have questions for this exam. Maybe you can try one of our other features :)"
            messenger_bot.send_action(action='typing_on', recipient_id=messenger_id)
            messenger_bot.send_text_message(recipient_id=messenger_id, message=message)

            return

        if len(questions_ids) >10:
            current_questions_ids = random.sample(questions_ids, 10)
        else:
            current_questions_ids = questions_ids
        current_bot_user.current_questions_ids = json.dumps(current_questions_ids)
        current_bot_user.save()

    else:
        json_data=json.loads(current_bot_user.json_store)
        try:
            difficulty = json_data['difficulty_level']
        except KeyError as err:
            difficulty = None
            logger.warning(err)

        try:
            language_code = json_data['language_code']
        except KeyError as err:
            language_code = None
            logger.warning(err)

        questions_ids = current_questions_ids

    if questions_done >= len(current_questions_ids):

        current_profile_data = get_profile_data(messenger_id=messenger_id)

        # first send a message to indicate whether the answer was wrong or right
        messenger_bot.send_action(recipient_id=messenger_id, action="typing_on")
        if 'text_message' in state:
            messenger_bot.send_action(recipient_id=messenger_id, action='typing_on')
            messenger_bot.send_text_message(recipient_id=messenger_id, message=state['text_message'])

        elif 'button_message' in state:
            messenger_bot.send_action(recipient_id=messenger_id, action='typing_on')
            messenger_bot.send_button_message(recipient_id=messenger_id, buttons=state['buttons'], text=state['button_message'])

        #if this was sent through a challenge
        if current_bot_user.quiz_challenged:
            handle_quiz_challenge(messenger_id)
            
        elif current_bot_user.solving_course_quiz:
            current_bot_user.solving_course_quiz=False
            current_bot_user.questions_done=0
            current_bot_user.save()
      
            messenger_bot.send_text_message(recipient_id=messenger_id, message='You are done with that quiz :)')
        
        elif current_bot_user.generated_quiz_challenged:
            quiz_data = json.loads(current_bot_user.quiz_data)
            challenger_bot_user=BotUser.objects.get(messenger_id=quiz_data['challenger_id'])
            challenged_score = str(current_bot_user.questions_right) + " out of " + str(current_bot_user.questions_done)

            quiz_results=json.loads(challenger_bot_user.generated_quiz_results)
            quiz_results['total_score']=quiz_results['total_score']+current_bot_user.questions_done

            quiz_results['average_score']=round((quiz_results['average_score']+current_bot_user.questions_right)/(quiz_results['total_score']/current_bot_user.questions_done),2)

            el1 = plain_element(
                title=current_profile_data['first_name'] + " " + current_profile_data['last_name'],
                image_url=current_profile_data['profile_picture_url']
            )

            el2=plain_element(
                title="Score",
                subtitle=challenged_score
            )

            el3=plain_element(
                title='Quiz Data',
                subtitle='Average Score: '+ str(quiz_results['average_score'])+ '\n'
                         'Total Score: '+ str(quiz_results['total_score'])
            )
            elements = [el1, el2, el3]

            s_button = share_button()

            current_bot_user.generated_quiz_challenged = False
            current_bot_user.quiz_data = None
            current_bot_user.save()

            #send a message to the challenged informing them  of their score

            message = "Your Score is: " + str(current_bot_user.questions_right) + ' out of ' + \
                      str(current_bot_user.questions_done)

            messenger_bot.send_action(recipient_id=messenger_id, action="typing_on")
            messenger_bot.send_text_message(recipient_id=messenger_id, message=message)

            #send  a message to the challenger informing them that this person completed the quiz
            message = current_profile_data['first_name'] + ' ' + current_profile_data[
                'last_name'] + ' completed your challenge. 👀 results 👇  :)'

            messenger_bot.send_text_message(recipient_id=quiz_data['challenger_id'], message=message)
            r=messenger_bot.send_list_message(recipient_id=quiz_data['challenger_id'], elements=elements,
                                                 buttons=[s_button])
            print(r)

        else:
            print(difficulty)
            print(language_code)
            message = "Your Score is: " + str(current_bot_user.questions_right) + ' out of ' + \
                      str(current_bot_user.questions_done)

            messenger_bot.send_action(recipient_id=messenger_id, action="typing_on")
            messenger_bot.send_text_message(recipient_id=messenger_id, message=message)

            if difficulty  and language_code:
                subtitle=current_profile_data['first_name']+" "+ current_profile_data['last_name']+ " sent you a programming quiz"
                payload={
                    'quiz_data':{
                        'challenger_id': current_bot_user.messenger_id,
                        'questions_right': current_bot_user.questions_right,
                        'questions_done_ids': current_bot_user.current_questions_ids,
                        'language_code': language_code,
                        'difficulty_level': difficulty
                    }
                }

                solve_url=bot_url+'?ref='+urllib.parse.quote(json.dumps(payload))

                solve_btn=web_button(
                    title='Try it',
                    url=solve_url
                )

                solve_buttons=[solve_btn]

                solve_element=plain_element(
                    title='Quiz Challenge',
                    subtitle=subtitle,
                    image_url=current_profile_data['profile_picture_url'],
                    buttons=solve_buttons
                )

                solve_elements=[solve_element]

                # Send a share template to the student prompting them to share the bot with their friends

                current_bot_user.questions_done=0
                current_bot_user.questions_right=0
                current_bot_user.current_questions_ids=json.dumps([])
                scores=json.loads(current_bot_user.scores)
                scores.append(current_bot_user.quiz_total)
                current_bot_user.scores=json.dumps(scores)
                current_bot_user.quiz_total=0
                current_bot_user.save()

                done_with_quiz(messenger_id=messenger_id, elements=solve_elements)


    else:
        if questions_done >0:
            if 'text_message' in state:
                messenger_bot.send_action(recipient_id=messenger_id, action='typing_on')
                messenger_bot.send_text_message(recipient_id=messenger_id, message=state['text_message'])

            elif 'button_message' in state:
                messenger_bot.send_action(recipient_id=messenger_id, action='typing_on')
                messenger_bot.send_button_message(recipient_id=messenger_id, buttons=state['buttons'],
                                                  text=state['button_message'])

        current_question_id = current_questions_ids[current_bot_user.questions_done]
        try:
            current_question = ProgrammingQuestion.objects.get(id=current_question_id)
        except:
            current_question = ProgrammingQuestion.objects.get(id=random.choice(questions_ids))

        if current_question.difficulty_level == 'simple':
            current_bot_user.possible_total+=1
            current_bot_user.save()

        elif current_question.difficulty_level == 'intermediate':
            current_bot_user.possible_total+=3
            current_bot_user.save()

        elif current_question.difficulty_level == 'difficult':
            current_bot_user.possible_total +=5
            current_bot_user.save()

        current_bot_user.questions_done += 1
        current_bot_user.save()

        if current_question.image:
            image_url = current_question.image.url
            messenger_bot.send_image_url(recipient_id=messenger_id, image_url=image_url)

        answers = current_question.answers.all()


        list = [i for i in range(len(answers))]
        random.shuffle(list)

        text = "\n " + str(current_bot_user.questions_done) + "⬇️ \n " + current_question.question

        quick_replies = []

        for choice in list:
            answer = answers[choice]
            payload = {}
            payload['answer_id'] = str(answer.id)
            quick_reply = text_quick_reply(title=answer.answer, payload=json.dumps(payload))
            quick_replies.append(quick_reply)

        message = {
            'text': text,
            'quick_replies': quick_replies
        }

        messenger_bot.send_action(recipient_id=messenger_id, action="typing_on")
        re=messenger_bot.send_message(message=message, recipient_id=messenger_id)
        print(re)

def handle_quiz_challenge(messenger_id):

    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    current_profile_data = json.loads(current_bot_user.profile_details)
    quiz_data = json.loads(current_bot_user.quiz_data)
    challenger_profile_data = get_profile_data(quiz_data['challenger_id'])
    challenger_score = str(quiz_data['questions_right']) + " out of " + str(current_bot_user.questions_done)
    challenged_score = str(current_bot_user.questions_right) + " out of " + str(current_bot_user.questions_done)

    el1 = plain_element(
        title=challenger_profile_data['first_name'] + " " + challenger_profile_data['last_name'],
        subtitle=challenger_score,
        image_url=challenger_profile_data['profile_picture_url']
    )

    el2 = plain_element(
        title=current_profile_data['first_name'] + " " + current_profile_data['last_name'],
        subtitle=challenged_score,
        image_url=current_profile_data['profile_picture_url']
    )
    elements = [el1, el2]

    s_button = share_button()

    current_bot_user.quiz_challenged = False
    current_bot_user.quiz_data = None
    current_bot_user.save()

    messenger_bot.send_plainlist_message(recipient_id=messenger_id, elements=elements, buttons=[s_button])

    message = current_profile_data['first_name'] + ' ' + current_profile_data[
        'last_name'] + ' completed your challenge. 👀 results 👇  :)'

    messenger_bot.send_text_message(recipient_id=quiz_data['challenger_id'], message=message)
    messenger_bot.send_plainlist_message(recipient_id=quiz_data['challenger_id'], elements=elements, buttons=[s_button])

def get_profile_data(messenger_id):
    current_bot_user=BotUser.objects.get(messenger_id=messenger_id)
    profile_data = json.loads(current_bot_user.profile_details)
    try:
        first_name = profile_data['first_name']
    except:
        first_name = ''

    try:
        last_name = profile_data['last_name']
    except:
        last_name = ''

    try:
        profile_picture_url = profile_data['profile_pic']
    except:
        profile_picture_url = None

    res={
        'first_name': first_name,
        'last_name': last_name,
        'profile_picture_url': profile_picture_url
    }

    return res


def done_with_quiz(messenger_id, elements):
    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    scores = json.loads(current_bot_user.scores)
    current_total = sum(scores)
    current_percent = (current_total/current_bot_user.possible_total)*100
    title = "Your Quizes Score:  " + str(round(current_percent, 2))+"%"
    subtitle = "Wanna challenge someone with this Quiz? Click Share ⬇️"

    s_button = share_with_template(elements=elements)

    element = plain_element(
        title=title,
        subtitle=subtitle,
        image_url='https://www.mycreditmonitor.co.uk/img/seo/icon_arrowCircle.png',
        buttons=[s_button]
    )

    menu_elements = [element]
    messenger_bot.send_action(action='typing_on', recipient_id=messenger_id)
    messenger_bot.send_generic_message(recipient_id=messenger_id, elements=menu_elements)

    send_post_quiz_replies(messenger_id=messenger_id)


def check_answer(answer_id, question_id):
    ans = ProgrammingQuestionAnswer.objects.get(id=answer_id)
    qs = ProgrammingQuestion.objects.get(id=question_id)
    if ans.state == '1':
        return True
    else:
        answers = qs.answers.all()

        for ans in answers:
            if ans.state == '1':
                return (ans.answer)

def generate_quiz(messenger_id):

    current_profile_data = get_profile_data(messenger_id=messenger_id)
    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    questions_data = get_questions_data(current_bot_user)
    questions_ids, language_code, difficulty = questions_data[1],questions_data[2], questions_data[3]

    if len(questions_ids) >10:
        questions_ids = random.sample(questions_ids, 10)

    subtitle = current_profile_data['first_name'] + " " + current_profile_data[
        'last_name'] + " wants you to try a programming quiz"
    payload = {
        'generated_q_data': {
            'challenger_id': messenger_id,
            'questions_ids': questions_ids,
            'language_code': language_code,
            'difficulty_level': difficulty
        }
    }

    solve_url = bot_url + '?ref=' + urllib.parse.quote(json.dumps(payload))

    solve_btn = web_button(
        title='Try it',
        url=solve_url
    )

    solve_buttons = [solve_btn]

    solve_element = plain_element(
        title='Quiz Challenge',
        subtitle=subtitle,
        image_url=current_profile_data['profile_picture_url'],
        buttons=solve_buttons
    )

    solve_elements = [solve_element]

    share_btn=share_with_template(solve_elements)

    message="We generated a quiz with 10 questions for you." \
            " You can share it to a group and you will be notified when any person solves the quiz :)"

    messenger_bot.send_action(recipient_id=messenger_id, action="typing_on")
    messenger_bot.send_button_message(recipient_id=messenger_id, buttons=[share_btn], text=message)


def send_code_segment_quiz(messenger_id, segment_id):
    current_bot_user = BotUser.objects.get(messenger_id=messenger_id)
    current_segment = CourseSegment.objects.get(id=segment_id)
    quiz_questions = current_segment.programming_questions.all()

    current_bot_user.current_questions_ids = json.dumps([question.id for question in quiz_questions])
    current_bot_user.solving_course_quiz = True
    current_bot_user.questions_right = 0
    current_bot_user.questions_done = 0
    current_bot_user.save()
    send_question(messenger_id, state={'text_message': ''})

