import factory
import string
import random
import datetime
import json
from faker import Factory
from factory import fuzzy
from faker import Faker

from django.utils import timezone

from .models import (
    FacebookUser,
    ProgrammingLanguage,
    ProgrammingQuestion,
    ProgrammingCategory,
    BotUser,
    CodingQuestion,
    ProgrammingQuestionAnswer,
    CodingResult
)


faker = Factory.create()
fake = Faker()


def get_random_number():
    return ''.join(random.choice(string.digits) for i in range(15))


def get_random_url():
    return 'https://www.facebook.com/'+ faker.word()


json_data = {"category_id": 1, "difficulty_level": "simple", "language_code": "30"}
quiz_data = {"challenger_id": "1528075240606741", "questions_done_ids": [0,1,2],
             "questions_right": 4, "difficulty_level": "simple", "language_code": "30"}
question_data = {"challenger_score": 100.0, "question_id": 6, "challenger_id": "1528075240606741"}
generated_quiz_results = {"total_score": 0, "average_score": 0}

profile_details = {"last_name": "Wagura",
                   "gender": "male",
                   "profile_pic": "https://scontent.xx.fbcdn.net/v/t31.0-1/18620745_1018895178241712_4"
                                  "268700238720152377_o.jpg?oh=ebdceba23337b445a0a52d9d7e31a86c&oe=5A6C1C96",
                   "id": "1528075240606741",
                   "locale": "en_US",
                   "first_name": "Joseph",
                   "timezone": 1
                 }

coding_question_data = {
            "title": "Division of Numbers",
            "difficulty_level": "difficult",
            "question": "You are given two numbers. Divide them and display the answer",
            "sample_input": json.dumps(["6 2"]),
            "sample_output": json.dumps(["3"]),
            "solution_language": '30',
            "solution": "nums=[int(a) for a in input().split()]\nans=nums[0]/nums[1]\nprint(int(ans))",
            "input": json.dumps(["6 2", "22 2", "15 3"])
}

coding_result_data = {
            'coder_facebook_id': "67",
            'question_solved_id': 7,
            'last_testcase_passed_index': 3,
            'coder_source_code': "print(5)",
            'error' : None,
            'scores' : "[]",
            'possible_total': 0
}


class FacebookUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FacebookUser

    facebook_id = factory.LazyFunction(get_random_number)
    name = factory.Faker('name')
    email = factory.Faker('email')
    profile_picture_url = factory.LazyFunction(get_random_url)


class BotUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = BotUser

    facebook_user = factory.SubFactory(FacebookUserFactory)
    messenger_id = factory.LazyFunction(get_random_number)
    profile_details = json.dumps(profile_details)
    json_store = json.dumps(json_data)
    current_questions_ids = json.dumps([1])
    questions_done = fuzzy.FuzzyInteger(0, 1000)
    questions_right = fuzzy.FuzzyInteger(50, 100)
    possible_total = fuzzy.FuzzyInteger(0, 50)
    quiz_total = fuzzy.FuzzyInteger(100)
    scores = json.dumps([1, 2, 3])
    quiz_challenged = fuzzy.FuzzyChoice([0, 1])
    quiz_data = json.dumps(quiz_data)
    question_challenged = fuzzy.FuzzyChoice([0, 1])
    generated_quiz_challenged = fuzzy.FuzzyChoice([0, 1])
    generating_quiz = fuzzy.FuzzyChoice([0, 1])
    generated_quiz_results = json.dumps(generated_quiz_results)
    question_data = json.dumps(generated_quiz_results)
    solving_course_quiz = fuzzy.FuzzyChoice([0, 1])


class ProgrammingCategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProgrammingCategory

    name = fuzzy.FuzzyChoice(['General', 'Web'])
    published = fuzzy.FuzzyChoice([0, 1])


class ProgrammingLanguageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProgrammingLanguage

    category = factory.SubFactory(ProgrammingCategoryFactory)
    name = fuzzy.FuzzyChoice(['python', 'java', 'javascript'])
    code = fuzzy.FuzzyChoice(['30', '40', '50'])
    logo = factory.django.ImageField()
    published = fuzzy.FuzzyChoice([0, 1])


class ProgrammingQuestionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProgrammingQuestion

    author = factory.SubFactory(FacebookUserFactory)
    language = factory.SubFactory(ProgrammingLanguageFactory)
    question = fake.sentence()
    difficulty_level = fuzzy.FuzzyChoice(['simple', 'intermediate', 'difficult'])
    explanation = fake.sentence()
    image = factory.django.ImageField()


class ProgrammingQuestionAnswerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProgrammingQuestionAnswer

    related_question = factory.SubFactory(ProgrammingQuestionFactory)
    answer = fake.word()
    state = fuzzy.FuzzyChoice(['1', '2'])


class CodingQuestionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CodingQuestion

    author = factory.SubFactory(FacebookUserFactory)
    title = fake.word()
    difficulty_level = fuzzy.FuzzyChoice(['simple', 'intermediate', 'difficult'])
    question = fake.sentence()
    sample_input = coding_question_data['sample_input']
    sample_output = coding_question_data['sample_output']
    solution_language = coding_question_data['solution_language']
    solution = coding_question_data['solution']
    input = coding_question_data['input']


class CodingResultFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CodingResult

    coder_facebook_id = "123456"
    question_solved_id = fuzzy.FuzzyInteger(0, 1000)
    last_testcase_passed_index = fuzzy.FuzzyInteger(0, 1000)
    coder_source_code = coding_result_data['coder_source_code']
    error = coding_result_data['error']
    scores = coding_result_data['scores']
    possible_total = fuzzy.FuzzyInteger(0,1000)



