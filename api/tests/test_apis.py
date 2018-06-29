import json

from django.urls import reverse
from django.contrib.sites.models import Site
from rest_framework.test import APIClient, APITestCase

from hway import factories
from hway.models import (
    FacebookUser,
    CodingQuestion,
    CodingResult
)
current_domain = Site.objects.get_current().domain



class TestFacebookUserCreateApiView(APITestCase):

    """
    Can we create a new facebook user??

    """

    def setUp(self):

        self.facebook_user1 = factories.FacebookUserFactory()
        self.facebook_user2 = factories.FacebookUserFactory()
        self.facebook_user3 = factories.FacebookUserFactory()

    def test_facebook_user_create_api_view(self):

        data = {
            'facebook_id': '982383743824382',
            'name': 'William',
            'email': 'joseritch45@gmail.com',
            'profile_picture_url': 'https://www.facebook.com/klsmfssnfosinfosd'
        }
        client = APIClient()
        response = client.post('/api/v1/facebook_users/create', data=data, format='json')
        self.assertIn('success', response.json())

    def test_facebook_list_api_view(self):

        client = APIClient()
        response = client.get('/api/v1/facebook_users')
        self.assertEqual(len(response.json()), 3)

    def test_facebook_user_update_api_view(self):

        client = APIClient()

        data = {
            'email': 'j4576@gmail.com',
            'name': 'josewails',
            'facebook_id': '8127101271812'
        }

        facebook_id = self.facebook_user1.facebook_id

        response = client.put('/api/v1/facebook_users/'+ facebook_id + '/update', data=data, format='json')

        #  Assert that updating a facebook user returns a code of 200

        self.assertEqual(response.status_code, 200)

        #  Assert that the update user has the email in the data above

        self.assertEqual('j4576@gmail.com', FacebookUser.objects.get(facebook_id='8127101271812').email)

    def test_facebook_user_retrieve(self):

        client = APIClient()
        facebook_id = self.facebook_user1.facebook_id

        response = client.get('/api/v1/facebook_users/' + facebook_id)

        # Assert that trying to retrieve a certain user returns with a code of 200

        self.assertEqual(response.status_code, 200)

        # Assert the email of the retrieved facebook user matches the expected email

        self.assertEqual(response.json()['email'], self.facebook_user1.email)

    def test_delete_facebook_user_api_view(self):

        client = APIClient()
        facebook_id = self.facebook_user1.facebook_id

        # delete the facebook user with the the above facebook id

        delete_response = client.delete('/api/v1/facebook_users/' + facebook_id + '/delete')
        self.assertEqual(delete_response.status_code, 204)

        # check to ensure that the facebook user has been deleted

        retrieve_response = client.get('/api/v1/facebook_users/' + facebook_id)
        self.assertEqual(retrieve_response.status_code, 404)




class TestCodingQuestionAPI(APITestCase):

    """
    Test all Coding Question API endpoints.

    """

    def setUp(self):

        self.facebook_user = factories.FacebookUserFactory()
        self.coding_questions = []

        for i in range(10):
            self.coding_questions.append(factories.CodingQuestionFactory(author=self.facebook_user))

    def test_coding_question_create(self):
        client = APIClient()

        facebook_id = self.facebook_user.facebook_id

        coding_question_data = {
            'facebook_id': facebook_id,
            "title": "Division of Numbers",
            "difficulty_level": "difficult",
            "question": "You are given two numbers. Divide them and display the answer",
            "sample_input": json.dumps(["6 2"]),
            "sample_output": json.dumps(["3"]),
            "solution_language": '30',
            "solution": "nums=[int(a) for a in input().split()]\nans=nums[0]/nums[1]\nprint(int(ans))",
            "input": json.dumps(["6 2", "22 2", "15 3"])
        }

        # Try creating a question
        response = client.post('/api/v1/coding_questions/create', data=coding_question_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())

    def test_coding_question_list_api_view(self):
        client = APIClient()

        response = client.get('/api/v1/coding_questions')

        # assert that the response return with a status code of 200

        self.assertEqual(response.status_code, 200)

        # Assert that there are 10 questions

        self.assertEqual(len(response.json()), 10)

    def test_coding_question_difficulty_filtered_list_api_view(self):
        client = APIClient()

        response = client.get('/api/v1/coding_questions/difficulty_level/simple')
        simple_count = CodingQuestion.objects.filter(difficulty_level='simple').count()

        # Assert the number of simple questions retrieved is the same as the number of

        self.assertEqual(len(response.json()), simple_count)

    def test_coding_question_retrive_view(self):
        client = APIClient()

        question_id = self.coding_questions[0].id
        question_difficulty = self.coding_questions[0].difficulty_level

        response = client.get('/api/v1/coding_questions/'+ str(question_id))

        # Assert that it returns with a response of 200.

        self.assertEqual(response.status_code, 200)

        # Assert the difficulty level of the above question is the same as the retrieved one.

        self.assertEqual(response.json()['difficulty_level'], question_difficulty)


class TestCodingResultAPI(APITestCase):

    def setUp(self):

        self.coding_results = []

        for i in range(5):
            self.coding_results.append(factories.CodingResultFactory(coder_facebook_id='12346476234'))

    def test_facebook_user_coding_result_list(self):

        client = APIClient()
        facebook_id = self.coding_results[0].coder_facebook_id

        response = client.get('/api/v1/coding_results/' + facebook_id)

        # Assert that the above request returns with a status code of 200

        self.assertEqual(response.status_code, 200)

        # Assert that the above there are five coding results as expected

        self.assertEqual(len(response.json()), 5)


class TestProgrammingLanguageAPI(APITestCase):

    def setUp(self):
        facebook_user = factories.FacebookUserFactory()
        programming_category = factories.ProgrammingCategoryFactory()
        programming_language = factories.ProgrammingLanguageFactory(category=programming_category)

        self.programming_questions = []

        for i in range(5):
            self.programming_questions.append(factories.ProgrammingQuestionFactory(author=facebook_user, language=programming_language))

    def test_programming_question_list(self):

        client = APIClient()

        response = client.get('/api/v1/programming_questions')

        # Assert that the above request returns with a status code of 200

        self.assertEqual(response.status_code, 200)

        # Assert that the number of programming questions is 5

        self.assertEqual(len(response.json()[0]['questions']), 5)

