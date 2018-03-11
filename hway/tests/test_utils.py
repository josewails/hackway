from django.test import TestCase
from hway.utils import get_individual_score, validate_ground_code
from hway.models import CodingResult,BotUser, FacebookUser
import json

class TestGetIndividualScore(TestCase):

    """"""

    def setUp(self):

        profile_details =  {
            "last_name": "Wagura",
           "gender": "male",
           "profile_pic": "https://scontent.xx.fbcdn.net/v/t31.0-1/18620745_1018895178241712_4268700238720152377_o.jpg?oh=ebdceba23337b445a0a52d9d7e31a86c&oe=5A6C1C96",
            "id": "1528075240606741",
            "locale": "en_US",
            "first_name": "Joseph",
            "timezone": 1
        },

        facebook_user = FacebookUser.objects.create(
            facebook_id='67',
            name='Joseph Gitonga Wagura'
        )

        BotUser.objects.create(
            facebook_user = facebook_user,
            messenger_id="1528075240606741",
            profile_details = json.dumps(profile_details),
            current_questions_ids= json.dumps([5, 6, 7]),
            questions_done= 1,
            questions_right = 0,
            possible_total = 24,
            quiz_total= 0,
            scores = json.dumps([2,2,1,1,1,5]),
            quiz_challenged=False,
            quiz_data= "{}",
            question_challenged= False,
            generated_quiz_challenged = False,
            generating_quiz= False,
            generated_quiz_results="{}",
            question_data ="{}",
            solving_course_quiz= True,
            course_data = "{}"
        )

        CodingResult.objects.create(
            coder_facebook_id="67",
            question_solved_id=5,
            last_testcase_passed_index=3,
            coder_source_code= None,
            error=None,
            scores=json.dumps([2,1,3]),
            possible_total= 12
        )



    def test_get_individual_score(self):
        res = get_individual_score('67', '1528075240606741')
        self.assertIn('quiz_score', res)
        self.assertIn('challenge_score', res)
        self.assertIn('overall_score', res)
        self.assertEqual(res['quiz_score'],50.0)
        self.assertEqual(res['challenge_score'],50.0)
        self.assertEqual(res['overall_score'],50.0)

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

