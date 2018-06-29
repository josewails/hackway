from django.test import TestCase
import json
from unittest.mock import patch
from pymessenger.bot import Bot
from messenger.views import (
    handle_post_back,
    handle_quick_reply
    )

from hway import factories


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

        self.bot_user = factories.BotUserFactory()
        self.programming_category = factories.ProgrammingCategoryFactory()

    # Test whether the 'get_started' payload is well handled

    @patch.object(Bot, 'send_generic_message')
    @patch.object(Bot, 'send_action')
    @patch.object(Bot, 'send_text_message')
    def test_handle_get_started(self,
                                mock_send_text_message,
                                mock_send_action,
                                mock_send_generic_message):

        handle_post_back(recipient_id=self.bot_user.messenger_id, post_back=self.get_started_post_back)

        # Assert that the send_text_message is called once

        self.assertEqual(mock_send_text_message.call_count, 1)

        # Assert that the send_generic_message is called once

        self.assertEqual(mock_send_generic_message.call_count, 1)

        # Assert that the send_action is called once

        self.assertEqual(mock_send_action.call_count, 1)

    # Test whether the 'options' payload is well handled

    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_handle_options_post_back(self,
                                      mock_send_action,
                                      mock_send_message):

        handle_post_back(recipient_id=self.bot_user.messenger_id, post_back=self.options_post_back)

        # Test that the send action is called once

        self.assertEqual(mock_send_action.call_count, 1)

        # Test that the send_message is called once

        self.assertEqual(mock_send_message.call_count, 1)

    # Test whether 'programming_questions' payload really works

    @patch.object(Bot, 'send_button_message')
    @patch.object(Bot, 'send_action')
    def test_handle_programming_questions_post_back(self,
                                                    mock_send_action,
                                                    mock_send_button_message):

        handle_post_back(recipient_id=self.bot_user.messenger_id, post_back=self.programming_questions_post_back)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_button_message.call_count, 1)

    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_handle_language_code_post_back(self,
                                            mock_send_action,
                                            mock_send_message):
        handle_post_back(recipient_id=self.bot_user.messenger_id, post_back=self.language_code_post_back)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_message.call_count, 1)

    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_programming_multiple_answer_post_back(self,
                                                   mock_send_action,
                                                   mock_send_message):

        handle_post_back(recipient_id=self.bot_user.messenger_id, post_back=self.programming_multiple_answer_post_back)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_message.call_count, 1)

    @patch.object(Bot, 'send_generic_message')
    @patch.object(Bot, 'send_action')
    def test_send_menu(self,
                       mock_send_action,
                       mock_send_generic_message
                       ):
        handle_post_back(recipient_id=self.bot_user.messenger_id, post_back=self.main_menu_postback)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_generic_message.call_count, 1)

    @patch.object(Bot, 'send_text_message')
    @patch.object(Bot, 'send_button_message')
    @patch.object(Bot, 'send_action')
    def test_handle_how_to_challenge_payload(self,
                                             mock_send_action,
                                             mock_send_button_message,
                                             mock_send_text_message):
        handle_post_back(recipient_id=self.bot_user.messenger_id, post_back=self.how_to_challenge_postback)

        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_button_message.call_count, 1)
        self.assertEqual(mock_send_text_message.call_count, 1)

    @patch('messenger.utils.handle_programming_multiple_answer_payload')
    def test_generate_quiz_paylaod(self, mock_handle_multiple_answer_payload):
        handle_post_back(recipient_id=self.bot_user.messenger_id, post_back=self.generating_quiz_post_back)

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

        self.difficult_level_quick_reply = {
            'difficulty_level': 'simple'
        }

        self.bot_user = factories.BotUserFactory()
        self.programming_category = factories.ProgrammingCategoryFactory()
        self.programming_language = factories.ProgrammingLanguageFactory(category=self.programming_category)
        self.programming_question = factories.ProgrammingQuestionFactory(language=self.programming_language)

    # Test whether 'programming_questions' payload really works

    @patch.object(Bot, 'send_button_message')
    @patch.object(Bot, 'send_action')
    def test_handle_programming_questions_quick_reply(self, mock_send_action, mock_send_button_message):

        handle_quick_reply(recipient_id=self.bot_user.messenger_id,
                           quick_reply_message=self.programming_questions_quick_reply)

        # Assert send_action is called only once

        self.assertEqual(mock_send_action.call_count, 1)

        # Assert send_button_message is called only once

        self.assertEqual(mock_send_button_message.call_count, 1)

    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_handle_language_code_post_quick_reply(self, mock_send_action, mock_send_message):

        handle_quick_reply(recipient_id=self.bot_user.messenger_id, quick_reply_message=self.language_code_quick_reply)

        # assert that the send_action is called only once

        self.assertEqual(mock_send_action.call_count, 1)

        # assert that the send_message is called only once

        self.assertEqual(mock_send_message.call_count, 1)

    @patch.object(Bot, 'send_message')
    @patch.object(Bot, 'send_action')
    def test_programming_multiple_answer_quick_reply(self, mock_send_action, mock_send_message):
        handle_quick_reply(recipient_id=self.bot_user.messenger_id,
                           quick_reply_message=self.programming_multiple_answer_quick_reply)

        # assert that send_action is called only once

        self.assertEqual(mock_send_action.call_count, 1)

        # assert that send_message is called only once

        self.assertEqual(mock_send_message.call_count, 1)

    @patch.object(Bot, 'send_generic_message')
    @patch.object(Bot, 'send_action')
    def test_send_menu(self, mock_send_action, mock_send_generic_message):
        handle_quick_reply(recipient_id=self.bot_user.messenger_id, quick_reply_message=self.main_menu_quick_reply)

        # assert that send_action is called only once

        self.assertEqual(mock_send_action.call_count, 1)

        # assert that the send_generic_message is called only once

        self.assertEqual(mock_send_generic_message.call_count, 1)

    @patch.object(Bot, 'send_generic_message')
    @patch.object(Bot, 'send_text_message')
    @patch.object(Bot, 'send_action')
    def test_handle_category_id_quick_reply(self, mock_send_action, mock_send_text_message,
                                            mock_send_generic_message):
        handle_quick_reply(recipient_id=self.bot_user.messenger_id, quick_reply_message=self.category_id_quick_reply)
        self.assertEqual(mock_send_action.call_count, 1)
        self.assertEqual(mock_send_generic_message.call_count, 1)
        self.assertEqual(mock_send_text_message.call_count, 1)
