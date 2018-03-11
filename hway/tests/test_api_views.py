from django.urls import reverse
from django.contrib.sites.models import Site
from hway.models import (
    FacebookUser,
    CodingQuestion,
    CodingResult,
    ProgrammingQuestion,
    ProgrammingLanguage
)
from rest_framework.test import APITestCase, RequestsClient
import json
current_domain = Site.objects.get_current().domain


class TestFacebookUserCreateApiView(APITestCase):

    """
    Can we create a new facebook user??

    """

    def setUp(self):

        self.facebook_user1 = {
            'facebook_id': '1303031013010013',
            'name': 'Joseph Gitonga Wagura',
            'email': 'j45@gmail.com'
        }

        self.facebook_user2 = {
            'facebook_id': '13030310100101',
            'name': 'Fracis Wagura',
            'email': 'francis45@gmail.com'
        }
        self.updated_facebook_user1 = {
            'facebook_id': '1303031013010013',
            'name': 'Joseph Gitonga Wagura',
            'email': 'j4576@gmail.com'
        }

        self.create_facebook_user_url = current_domain+reverse('create_facebook_user')
        self.facebook_list_url = current_domain + reverse('facebook_users_list')
        self.retrieve_facebook_user_url = current_domain + '/facebook_users/1303031013010013'
        self.delete_facebook_url = current_domain + '/facebook_users/1303031013010013/delete'

    def test_facebook_user_create_api_view(self):

        # print(self.url)
        client = RequestsClient()
        response = client.post(self.create_facebook_user_url, data=self.facebook_user1)
        self.assertIn('success', response.json())

    def test_facebook_list_api_view(self):
        client = RequestsClient()
        client.post(self.create_facebook_user_url, data=self.facebook_user1)
        client.post(self.create_facebook_user_url, data=self.facebook_user2)

        all_facebook_users = client.get(self.facebook_list_url).json()
        self.assertEqual(len(all_facebook_users), 2)

    def test_facebook_user_update_api_view(self):

        client = RequestsClient()
        client.post(self.create_facebook_user_url, data=self.facebook_user1)
        client.post(self.create_facebook_user_url, data=self.facebook_user2)

        facebook_id = FacebookUser.objects.get(email='j45@gmail.com').facebook_id
        update_url = current_domain+'/facebook_users/'+facebook_id+'/update'

        response = client.put(update_url, data=self.updated_facebook_user1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('j4576@gmail.com', FacebookUser.objects.get(facebook_id=facebook_id).email)

    def test_facebook_user_retrieve(self):
        client = RequestsClient()
        client.post(self.create_facebook_user_url, data=self.facebook_user1)
        client.post(self.create_facebook_user_url, data=self.facebook_user2)

        response = client.get(self.retrieve_facebook_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], 'j45@gmail.com')

    def test_delete_facebook_user_api_view(self):

        client = RequestsClient()
        client.post(self.create_facebook_user_url, data=self.facebook_user1)
        client.post(self.create_facebook_user_url, data=self.facebook_user2)

        # delete the facebook user with the id <1303031013010013>
        delete_response = client.delete(self.delete_facebook_url)
        self.assertEqual(delete_response.status_code, 204)

        # check to ensure that the facebook user with the id <1303031013010013> has been deleted
        retrieve_response = client.get(self.retrieve_facebook_user_url)
        self.assertEqual(retrieve_response.status_code, 404)


class TestCodingQuestionAPI(APITestCase):

    """
     Test the retrieval of all coding questions
    """

    def setUp(self):
        self.question1 = {
            'api_key': '1234',
            "title": "Division of Numbers",
            "difficulty_level": "difficult",
            "question": "You are given two numbers. Divide them and display the answer",
            "sample_input": json.dumps(["6 2"]),
            "sample_output": json.dumps(["3"]),
            "solution_language": '30',
            "solution": "nums=[int(a) for a in input().split()]\nans=nums[0]/nums[1]\nprint(int(ans))",
            "input": json.dumps(["6 2", "22 2", "15 3"])
        }

        self.question2 = {
            'api_key': '1234',
            "title": "Division of Numbers",
            "difficulty_level": "simple",
            "question": "You are given two numbers. Divide them and display the answer",
            "sample_input": json.dumps(["6 2"]),
            "sample_output": json.dumps(["3"]),
            "solution_language": '30',
            "solution": "nums=[int(a) for a in input().split()]\nans=nums[0]/nums[1]\nprint(int(ans))",
            "input": json.dumps(["6 2", "22 2", "15 3"])
        }

        self.facebook_user = {
            'facebook_id': '1303031013010013',
            'name': 'Joseph Gitonga Wagura',
            'email': 'j45@gmail.com',
            'private_api_key': '1234'
        }

        self.create_coding_question_url = current_domain + reverse('create_coding_question')
        self.create_facebook_user_url = current_domain + reverse('create_facebook_user')
        self.all_coding_questions_url = current_domain + reverse('all_coding_questions')
        self.coding_question_retrieve_url = current_domain + '/coding_questions/2'
        self.difficulty_filtered_coding_questions_url = current_domain + '/coding_questions/difficulty_level/simple'

    def test_coding_question_create(self):
        client = RequestsClient()

        # create a facebook user
        client.post(self.create_facebook_user_url, data=self.facebook_user)

        # the facebook user creates a question
        response = client.post(self.create_coding_question_url, data=self.question1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        self.assertEqual(CodingQuestion.objects.count(), 1)

    def test_coding_question_list_api_view(self):
        client = RequestsClient()

        # create a facebook user first
        client.post(self.create_facebook_user_url, data=self.facebook_user)

        # create two coding questions
        client.post(self.create_coding_question_url, data=self.question1)
        client.post(self.create_coding_question_url, data=self.question2)

        response = client.get(self.all_coding_questions_url)
        self.assertEqual(len(response.json()), 2)

    def test_coding_question_difficulty_filtered_list_api_view(self):
        client = RequestsClient()

        # create a facebook user first
        client.post(self.create_facebook_user_url, data=self.facebook_user)

        # create two coding questions
        client.post(self.create_coding_question_url, data=self.question1)
        client.post(self.create_coding_question_url, data=self.question2)

        response = client.get(self.difficulty_filtered_coding_questions_url)

        self.assertEqual(len(response.json()), 1)

    def test_coding_question_retrive_view(self):
        client = RequestsClient()

        # create a facebook user first
        client.post(self.create_facebook_user_url, data=self.facebook_user)

        # create two coding questions
        client.post(self.create_coding_question_url, data=self.question1)
        client.post(self.create_coding_question_url, data=self.question2)

        response = client.get(self.coding_question_retrieve_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['difficulty_level'], 'simple')


class TestCodingResultAPI(APITestCase):

    """
    Tests all the views related to the Coding Result Model

    """

    def setUp(self):
        CodingResult.objects.create(
            coder_facebook_id="67",
            question_solved_id=7,
            last_testcase_passed_index =3,
            coder_source_code= "print(5)",
            error=None,
            scores="[]",
            possible_total= 0
        )

        CodingResult.objects.create(
            coder_facebook_id="67",
            question_solved_id=8,
            last_testcase_passed_index=4,
            coder_source_code="print(5)",
            error=None,
            scores="[]",
            possible_total=0
        )



        self.coding_result_url = current_domain+'/coding_results/67'

    def test_facebook_user_coding_result_list(self):

        client = RequestsClient()
        response = client.get(self.coding_result_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()),2)

class TestProgrammingLanguageAPI(APITestCase):

    def setUp(self):

        facebook_user=FacebookUser.objects.create(
            facebook_id='1303031013010013',
            name='Joseph Gitonga Wagura',
            email='j4576@gmail.com'
        )

        programming_language1 = ProgrammingLanguage.objects.create(name='Python')
        programming_language2 = ProgrammingLanguage.objects.create(name="Java Script")

        ProgrammingQuestion.objects.create(
            course_segment=None,
            author=facebook_user,
            language=programming_language1,
            question="How do you check equality in python?",
            difficulty_level="simple",
            explanation="programming questions",
            image=None
        )

        ProgrammingQuestion.objects.create(
            course_segment=None,
            author=facebook_user,
            language=programming_language2,
            question="What is the command  for printing on screen in python?",
            difficulty_level="simple",
            explanation="programming questions",
            image=None
        )

        self.programming_language_list_url = current_domain+reverse('all_programming_languages')

    def test_programming_question_list(self):

        """
        Tests the retrieval of a list of all programming questions
        """

        client = RequestsClient()
        response = client.get(self.programming_language_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)




