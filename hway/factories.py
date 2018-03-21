import factory
import string
import random
import datetime
import json
from faker import Factory
from .models import (
    FacebookUser,
    ProgrammingLanguage,
    ProgrammingQuestion,
    ProgrammingCategory,
    Course,
    CourseSegment,
    BotUser
)
from factory import fuzzy

faker = Factory.create()

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
                   "profile_pic": "https://scontent.xx.fbcdn.net/v/t31.0-1/18620745_1018895178241712_4268700238720152377_o.jpg?oh=ebdceba23337b445a0a52d9d7e31a86c&oe=5A6C1C96",
                   "id": "1528075240606741",
                   "locale": "en_US",
                   "first_name": "Joseph",
                   "timezone": 1
                 }

course_data = {"data": []}
class FacebookUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = FacebookUser

    facebook_id = factory.LazyFunction(get_random_number)
    name = factory.Faker('name')
    email = factory.Faker('email')
    profile_picture_url = factory.LazyFunction(get_random_url)
    private_api_key = factory.LazyFunction(get_random_number)


class BotUserFactory(factory.DjangoModelFactory):

    class Meta:
        model = BotUser

    facebook_user = factory.SubFactory(FacebookUserFactory)
    messenger_id = '1528075240606741'
    profile_details = json.dumps(profile_details)
    json_store = json.dumps(json_data)
    current_questions_ids = json.dumps([1])
    questions_done = json.dumps([1])
    questions_right = fuzzy.FuzzyInteger(50,100)
    possible_total = fuzzy.FuzzyInteger(0,50)
    quiz_total = fuzzy.FuzzyInteger(100)
    scores = json.dumps([1,2,3])
    quiz_challenged = factory.Faker('quiz_challenged')
    quiz_data = json.dumps(quiz_data)
    question_challenged = factory.Faker('question_challenged')
    generated_quiz_challenged = factory.Faker('generated_quiz_challenged')
    generating_quiz = factory.Faker('generating_quiz')
    generated_quiz_results = json.dumps(generated_quiz_results)
    question_data = json.dumps(generated_quiz_results)
    solving_course_quiz = factory.Faker('solving_course_quiz')
    course_data = json.dumps(course_data)


class ProgrammingCategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProgrammingCategory

    name = factory.Faker('name')
    published = factory.LazyFunction(datetime.datetime.now)

class CourseFactory(factory.DjangoModelFactory):

    class Meta:
        model = Course

    name = factory.Faker('name')
    description = factory.Faker('description')

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for student in extracted:
                self.students.add(student)


class CourseSegmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = CourseSegment

    course = factory.SubFactory(CourseFactory)
    title = factory.Faker('title')
    intro = factory.Faker('intro')
    body = factory.Faker('body')


class ProgrammingLanguageFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProgrammingLanguage

    category = factory.SubFactory(ProgrammingCategoryFactory)
    name ='python'
    code = '30'
    logo = factory.django.ImageField()
    published = factory.LazyFunction(datetime.datetime.now)


class ProgrammingQuestionFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProgrammingQuestion

    course_segment = factory.SubFactory(CourseSegmentFactory)
    author = factory.SubFactory(FacebookUserFactory)
    language = factory.SubFactory(ProgrammingLanguageFactory)
    question = factory.Faker('question')
    difficulty_level = 'simple'
    explanation = factory.Faker('explanation')
    image = factory.django.ImageField()
