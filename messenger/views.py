import json


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from hway.models import(
    BotUser
)

from .utils import (
    handle_referral, handle_text_message, handle_post_back,
    create_new_bot_user, handle_quick_reply, send_results,
    handle_send_results_error
)


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


        # decodes the request and then converts it into json format
        request_body = request.body.decode('utf-8')
        req = json.loads(request_body)
        recipient_id = req['entry'][0]['messaging'][0]['sender']['id']

        # The following block of try-except blocks just checks for what type of message we are receiving
        try:
            BotUser.objects.get(messenger_id=recipient_id)
        except ObjectDoesNotExist:
            create_new_bot_user(recipient_id=recipient_id)

        try:
            post_back = req['entry'][0]['messaging'][0]['postback']
        except KeyError:
            post_back = None

        try:
            quick_reply_message = req['entry'][0]['messaging'][0]['message']['quick_reply']
        except KeyError:
            quick_reply_message = None

        try:
            text_message = req['entry'][0]['messaging'][0]['message']['text']
        except KeyError:
            text_message = None

        try:
            referral = req['entry'][0]['messaging'][0]['referral']
        except KeyError:
            referral = None

        try:
            get_started_referral = req['entry'][0]['messaging'][0]['postback']['referral']
        except KeyError as err:
            get_started_referral = None


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


@csrf_exempt
def send_coding_results(request):

    if request.method == 'POST':
        try:
            facebook_id = request.POST['facebook_id']
        except:
            facebook_id = None

        try:
            question_id = request.POST['question_id']
        except:
            question_id = None

        try:
            messenger_id = request.POST['messenger_id']
        except:
            messenger_id = None

        if facebook_id and question_id and messenger_id:
            send_results(messenger_id=messenger_id, facebook_id=facebook_id, question_id=question_id)

        else:
            handle_send_results_error(messenger_id, question_id)

    else:
        # handle error for other methods
        data = {
            'error': 'that method is not allowed'
        }

        return JsonResponse(data)

    return HttpResponse('Hello there')
