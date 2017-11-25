from django.test import TestCase

from django.test import TestCase
import requests
import json
import urllib.parse

import os, django



josewails='1307518072599510'
addie='1519445798105050'
facebook_id='1091795360951693',
question_id=21
webhook = 'http://localhost:8000/webhook'

def text_message_test(recipient_id, message):
    test_data = {
        'entry': [
            {
                'messaging': [
                    {
                        'message': {
                            'text': message
                        },
                        'sender': {
                            "id": recipient_id
                        }
                    }
                ]
            }
        ]
    }

    re = requests.post(url=webhook, json=test_data)
    print(re)


def referral_test(recipient_id,ref):
    test_data = {
        'entry': [
            {
                'messaging': [
                    {
                        'referral': {
                            'ref': ref
                        },
                        'sender': {
                            "id": recipient_id
                        }
                    }
                ]
            }
        ]
    }

    res=requests.post(url=webhook, json=test_data)
    print(res)


def test_button_postback(recipient_id, payload):
    test_data={
        'entry':[
            {
                'messaging':[
                    {
                        'postback': {
                            'payload': payload
                        },
                        'sender': {
                            "id": recipient_id
                        }
                    }
                ]
            }
        ]
    }

    re=requests.post(url=webhook, json=test_data)
    print(re)

def test_quick_reply(recipient_id, payload):
    test_data={
        'entry':[
            {
                'messaging':[
                    {
                        'message':{
                            'quick_reply':{
                                'payload': payload
                            }
                        },
                        'sender': {
                            "id": recipient_id
                        }
                    }
                ]
            }
        ]
    }

    re=requests.post(url=webhook, json=test_data)
    print(re)

json_data={
   'urun_id' : 4
}

payload={
    'category_id': 1
}

ref_data={
    'segment_id': 1
}

#test_button_postback(recipient_id=recipient_id, payload='how_to_challenge')
#test_quick_reply(recipient_id=recipient_id, payload='quiz_solve_more')
referral_test(recipient_id=josewails, ref=json.dumps(ref_data))
#text_message_test(recipient_id=recipient_id, message='hi')

