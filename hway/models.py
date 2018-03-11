from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
c_data={
    'data': []
}
import json


difficulty_level_choices=(
    ('simple', 'Simple'),
    ('intermediate', 'Intermediate'),
    ('difficult', 'Difficult')
)

answer_state_choices=(
    ('1', 'Right'),
    ('2', 'Wrong')
)

language_choices = ( 
    ('30', 'Python3'),
    ('5', 'Python2')
)

class FacebookUser(models.Model):
    facebook_id=models.CharField(max_length=100, unique=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(null=True)
    profile_picture_url=models.URLField(null=True, blank=True)
    private_api_key = models.CharField(max_length=10000, null=True)

    def __str__(self):
        return self.name

class BotUser(models.Model):
    facebook_user=models.ForeignKey(FacebookUser, null=True)
    messenger_id=models.CharField(max_length=100, unique=True)
    profile_details=models.CharField(max_length=1000000, null=True)
    json_store=models.CharField(max_length=1000000, default='{}')
    current_questions_ids=models.CharField(max_length=1000000, default='[]')
    questions_done=models.IntegerField(default=0)
    questions_right=models.IntegerField(default=0)
    possible_total=models.IntegerField(default=0)
    quiz_total=models.IntegerField(default=0)
    scores=models.CharField(max_length=1000000, default='[]')
    quiz_challenged=models.BooleanField(default=False)
    quiz_data=models.CharField(max_length=100000, null=True)
    question_challenged=models.BooleanField(default=False)
    generated_quiz_challenged=models.BooleanField(default=False)
    generating_quiz=models.BooleanField(default=False)
    generated_quiz_results=models.CharField(max_length=100000, null=True, default='{}')
    question_data=models.CharField(max_length=10000, null=True)
    solving_course_quiz=models.BooleanField(default=False)
    course_data=models.CharField(max_length=1000000, default=json.dumps(c_data))

    def __str__(self):
        return self.messenger_id

class Course(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    students=models.ManyToManyField(FacebookUser)

    def __str__(self):
        return self.name

class CourseSegment(models.Model):
    course=models.ForeignKey(Course, null=True, related_name='course_segments')
    title=models.CharField(max_length=100)
    intro=models.CharField(max_length=1000, null=True, blank=True)
    body=RichTextUploadingField()

    def __str__(self):
        return self.title

class CodingQuestion(models.Model):
    course_segment=models.ForeignKey(CourseSegment, null=True)
    author=models.ForeignKey(FacebookUser, null=True)
    title=models.CharField(max_length=50)
    difficulty_level=models.CharField(null=True,max_length=20,choices=difficulty_level_choices)
    question=models.TextField()
    sample_input=models.CharField(max_length=1000000)
    sample_output=models.CharField(max_length=100000, null=True)
    solution_language=models.CharField(max_length=4,null=True, choices=language_choices)
    solution=models.TextField(null=True)
    input=models.CharField(max_length=10000000)

    def __str__(self):
        return self.title


class CodingResult(models.Model):
    coder_facebook_id=models.CharField(max_length=100, null=True)
    question_solved_id=models.IntegerField(null=True)
    last_testcase_passed_index=models.IntegerField(default=0)
    coder_source_code=models.CharField(max_length=1000000, null=True)
    error=models.CharField(max_length=100000, null=True)
    scores=models.CharField(max_length=1000000,default='[]')
    possible_total=models.IntegerField(default=0)

    def __str__(self):
        return self.coder_facebook_id+"-"+str(self.question_solved_id)

class ProgrammingCategory(models.Model):
    name=models.CharField(max_length=100)
    published=models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural='Programming Categories'

class ProgrammingLanguage(models.Model):
    category=models.ForeignKey(ProgrammingCategory, null=True)
    code=models.CharField(max_length=3, null=True, unique=True)
    name=models.CharField(max_length=100, null=True, unique=True)
    logo=models.ImageField(upload_to='programming_languages_logos', null=True)
    published=models.BooleanField(default=False)
    def __str__(self):
        return self.name

class ProgrammingQuestion(models.Model):
    course_segment=models.ForeignKey(CourseSegment,null=True, blank=True, related_name='programming_questions')
    author=models.ForeignKey(FacebookUser, null=True)
    language=models.ForeignKey(ProgrammingLanguage, related_name='questions')
    question=models.TextField(null=True)
    difficulty_level=models.CharField(max_length=20, choices=difficulty_level_choices)
    explanation=models.TextField(null=True, blank=True)
    image=models.ImageField(null=True, blank=True, upload_to='programming_questions_images')

    def __str__(self):
        if self.language  and self.difficulty_level:
            return (self.language.name + " - " + self.difficulty_level)


class ProgrammingQuestionAnswer(models.Model):
    related_question=models.ForeignKey(ProgrammingQuestion, related_name='answers')
    answer=models.CharField(max_length=20)
    state=models.CharField(max_length=10, choices=answer_state_choices)

    def __str__(self):
        return self.answer




