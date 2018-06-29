from rest_framework import serializers
from hway.models import (
                    FacebookUser,
                    CodingQuestion,
                    CodingResult,
                    ProgrammingQuestion,
                    ProgrammingLanguage,
                    ProgrammingQuestionAnswer)

class FacebookUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=FacebookUser
        fields=[
            'facebook_id',
            'name',
            'email',
            'profile_picture_url'
        ]

class CodingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=CodingQuestion
        fields=[
            'id',
            'title',
            'difficulty_level',
            'question',
            'input',
            'sample_input',
            'sample_output'
        ]

class CodingQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CodingQuestion
        fields=[
            'id',
            'title',
            'difficulty_level',
            'question',
            'input',
            'solution',
            'solution_language',
            'sample_input',
            'sample_output'
        ]


class CodingResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=CodingResult
        fields=[
            'coder_facebook_id',
            'question_solved_id',
            'last_testcase_passed_index'
        ]


class ProgrammingQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProgrammingQuestionAnswer
        fields=('id','answer', 'state')


class ProgrammingQuestionSerializer(serializers.ModelSerializer):
    answers = ProgrammingQuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model=ProgrammingQuestion
        fields=( 'id','question', 'difficulty_level', 'answers')



class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    questions=ProgrammingQuestionSerializer(many=True, read_only=True)
    class Meta:
        model=ProgrammingLanguage
        fields=('code', 'name', 'questions')

class ProgrammingQuestionExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProgrammingQuestion
        fields=[
            'id'
        ]



