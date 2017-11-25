from django.test import TestCase

from django.test import TestCase
import requests
import json
import urllib.parse

import os, django



josewails='1528075240606741'
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






quiz_data={"challenger_id": josewails , "questions_right": 4, "questions_done_ids": "[0,1,2,3]", "language_code": "30", "difficulty_level": "simple"}
ref_data={}
ref_data['quiz_data']=quiz_data
#test_button_postback(recipient_id=recipient_id, payload='how_to_challenge')
#test_quick_reply(recipient_id=recipient_id, payload='quiz_solve_more')
referral_test(recipient_id=addie, ref=json.dumps(ref_data))
#text_message_test(recipient_id=recipient_id, message='hi')

