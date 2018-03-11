from django.test import TestCase, Client
from django.test import TestCase
import json
from pymessenger.bot import Bot
messenger_bot = Bot()

josewails='1528075240606741'
addie='1519445798105050'
facebook_id='1091795360951693',
question_id=21
webhook_url = 'http://localhost:8000/webhook'

def text_message(recipient_id, message):
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

    return test_data


def referral(recipient_id,ref):
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

    return test_data


def postback(recipient_id, payload):
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

    return test_data

def quick_reply(recipient_id, payload):
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

    return test_data


class TestWebhook(TestCase):

    def setUp(self):
        self.test_data = text_message(recipient_id=josewails, message='How are you nigga? ')


    def test_webhook(self):

        client = Client()
        response = client.post('/webhook', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(response.status_code,200)




