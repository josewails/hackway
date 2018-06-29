from django.test import TestCase
from unittest.mock import patch

from api.utils import (
    get_individual_score,
    validate_ground_code,
)

from hway import factories


class TestGetIndividualScore(TestCase):

    """"""

    def setUp(self):

        self.facebook_user = factories.FacebookUserFactory()
        self.bot_user = factories.BotUserFactory(facebook_user=self.facebook_user)
        self.coding_result = factories.CodingResultFactory()


    def test_get_individual_score(self):
        res = get_individual_score(self.facebook_user.facebook_id, self.bot_user.messenger_id)
        self.assertIn('quiz_score', res)
        self.assertIn('challenge_score', res)
        self.assertIn('overall_score', res)

class TestValidateGroundCode(TestCase):

    def setUp(self):

        self.source = "nums=[int(a) for a in input().split()]\nans=nums[0]/nums[1]\nprint(int(ans))"
        self.language_used = '30',
        self.test_cases = "[\"6 2\", \"22 2\", \"15 3\"]"
        self.output =  "3"

    def test_validate_ground_code(self):

        res = validate_ground_code(source=self.source, language_used=self.language_used, testcases=self.test_cases)
        self.assertIn('success', res)
        self.assertEqual(self.output, res['result'].strip())


