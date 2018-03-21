from django.test import TestCase, Client
import json
from unittest.mock import patch
from pymessenger.bot import Bot
from hway.bot_views import (
    handle_post_back,
    handle_quick_reply
    )
from hway.models import (
    BotUser,
    ProgrammingCategory,
    ProgrammingLanguage
)

josewails = '1528075240606741'
addie = '1519445798105050'
facebook_id = '1091795360951693',
question_id = 21
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


def referral(recipient_id, ref):
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
    test_data = {
        'entry': [
            {
                'messaging': [
                    {
                        'postback':  {
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
    test_data = {
        'entry': [
            {
                'messaging': [
                    {
                        'message': {
                            'quick_reply': {
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

    @patch.object(Bot, 'send_text_message')
    def test_webhook(self, mock_send_text_message):

        client = Client()
        response = client.post('/webhook', data=json.dumps(self.test_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_send_text_message.call_count, 1)


class TestHandlePostBack(TestCase):

    def setUp(self):
        self.get_started_post_back = {
            'payload': 'get_started'
        }

        self.options_post_back = {
            'payload': 'options'
        }

        self.programming_questions_post_back = {
            'payload': 'programming_questions'
        }

        self.language_code_post_back = {
            'payload': json.dumps({
                'language_code': '30'
            })
        }

        self.main_menu_postback = {
            'payload': 'main_menu'
        }

        self.programming_multiple_answer_post_back = {
            'payload': 'programming_multiple_answer'
        }

        self.how_to_challenge_postback = {
            'payload': 'how_to_challenge'
        }

        self.generating_quiz_post_back = {
            'payload': 'generate_quiz'
        }

        profile_details = {
            'first_name': "Joseph",
            "last_name": "Wagura"
        }

        json_data = {}

        BotUser.objects.create(messenger_id=josewails, profile_details=json.dumps(profile_details),
                               json_store=json.dumps(json_data))
        ProgrammingCategory.objects.create(name='General')

    # Test whether the 'get_started' payload is well handled
    @patch.object(Bot, 'send_generic_message')
    @patch.object(Bot, 'send_action')
    @patch.object(Bot, 'send_text_message')
    def test_handle_get_started(self,
                                mock_send_text_message,
                                mock_send_action,
                                mock_send_generic_message):

        handle_post_back(recipient_id=josewails, post_back=self.get_started_post_back)

        self.assertEqual(mock_send_text_message.call_count, 1)
        self.assertEqual(mock_send_generic_message.call_count, 1)
        self.assertEqual(mock_send_action.call_count, 1)

    # Test whether the 'options' payload is well handled
    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_handle_options_post_back(self,
                                      mock_send_action,
                                      mock_send_message):

        handle_post_back(recipient_id=josewails, post_back=self.options_post_back)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_message.call_count, 1)

    # Test whether 'programming_questions' payload really works
    @patch.object(Bot, 'send_button_message')
    @patch.object(Bot, 'send_action')
    def test_handle_programming_questions_post_back(self,
                                                    mock_send_action,
                                                    mock_send_button_message):

        handle_post_back(recipient_id=josewails, post_back=self.programming_questions_post_back)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_button_message.call_count, 1)

    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_handle_language_code_post_back(self,
                                            mock_send_action,
                                            mock_send_message):
        handle_post_back(recipient_id=josewails, post_back=self.language_code_post_back)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_message.call_count, 1)

    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_programming_multiple_answer_post_back(self,
                                                   mock_send_action,
                                                   mock_send_message):

        handle_post_back(recipient_id=josewails, post_back=self.programming_multiple_answer_post_back)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_message.call_count, 1)

    @patch.object(Bot, 'send_generic_message')
    @patch.object(Bot, 'send_action')
    def test_send_menu(self,
                       mock_send_action,
                       mock_send_generic_message
                       ):
        handle_post_back(recipient_id=josewails, post_back=self.main_menu_postback)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_generic_message.call_count, 1)

    @patch.object(Bot, 'send_text_message')
    @patch.object(Bot, 'send_button_message')
    @patch.object(Bot, 'send_action')
    def test_handle_how_to_challenge_payload(self,
                                             mock_send_action,
                                             mock_send_button_message,
                                             mock_send_text_message):
        handle_post_back(recipient_id=josewails, post_back=self.how_to_challenge_postback)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_button_message.call_count, 1)
        self.assertEqual(mock_send_text_message.call_count, 1)


    @patch('hway.bot_views.handle_programming_multiple_answer_payload')
    def test_generate_quiz_paylaod(self,mock_handle_multiple_answer_payload):
        handle_post_back(recipient_id=josewails, post_back=self.generating_quiz_post_back)

        self.assertEqual(
            mock_handle_multiple_answer_payload.call_count,
            1
        )


class TestHandleQuickReply(TestCase):

    def setUp(self):

        self.programming_questions_quick_reply = {
            'payload': 'programming_questions'
        }

        self.language_code_quick_reply = {
            'payload': json.dumps({
                'language_code': '30'
            })
        }

        self.main_menu_quick_reply = {
            'payload': 'main_menu'
        }

        self.programming_multiple_answer_quick_reply = {
            'payload': 'programming_multiple_answer'
        }

        self.category_id_quick_reply = {
            'payload': json.dumps({'category_id': 1})
        }

        self.difficult_level_quick_reply ={
            'difficulty_level': 'simple'
        }

        profile_details = {
            'first_name': "Joseph",
            "last_name": "Wagura"
        }

        json_data = {}

        BotUser.objects.create(messenger_id=josewails, profile_details=json.dumps(profile_details),
                               json_store=json.dumps(json_data))
        programming_category = ProgrammingCategory.objects.create(name='General')
        ProgrammingLanguage.objects.create(
            category=programming_category,
            name='Python',
            code='30'
        )

    # Test whether 'programming_questions' payload really works
    @patch.object(Bot, 'send_button_message')
    @patch.object(Bot, 'send_action')
    def test_handle_programming_questions_quick_reply(self,
                                                    mock_send_action,
                                                    mock_send_button_message):
        handle_quick_reply(recipient_id=josewails, quick_reply_message=self.programming_questions_quick_reply)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_button_message.call_count, 1)

    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_handle_language_code_post_quick_reply(self,
                                            mock_send_action,
                                            mock_send_message):
        handle_quick_reply(recipient_id=josewails, quick_reply_message=self.language_code_quick_reply)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_message.call_count, 1)

    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_programming_multiple_answer_quick_reply(self,
                                                   mock_send_action,
                                                   mock_send_message):
        handle_quick_reply(recipient_id=josewails, quick_reply_message=self.programming_multiple_answer_quick_reply)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_message.call_count, 1)

    @patch.object(Bot, 'send_generic_message')
    @patch.object(Bot, 'send_action')
    def test_send_menu(self,
                       mock_send_action,
                       mock_send_generic_message
                       ):
        handle_quick_reply(recipient_id=josewails, quick_reply_message=self.main_menu_quick_reply)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_generic_message.call_count, 1)


    @patch.object(Bot, 'send_generic_message')
    @patch.object(Bot, 'send_text_message')
    @patch.object(Bot, 'send_action')
    def test_handle_category_id_quick_reply(self,
                                mock_send_action,
                                mock_send_text_message,
                                mock_send_generic_message):
        handle_quick_reply(recipient_id=josewails, quick_reply_message=self.category_id_quick_reply)
        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_generic_message.call_count,1)
        self.assertEqual(mock_send_text_message.call_count, 1)
