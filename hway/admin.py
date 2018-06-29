from django.contrib import admin
from django import forms
import nested_admin
from ckeditor.widgets import  CKEditorWidget
from ckeditor_uploader.widgets import  CKEditorUploadingWidget
from .models import  (
    FacebookUser,
    CodingQuestion,
    CodingResult,
    BotUser,
    ProgrammingLanguage,
    ProgrammingQuestion,
    ProgrammingQuestionAnswer,
    ProgrammingCategory,
)


class AnswerInline(nested_admin.NestedTabularInline):
    model = ProgrammingQuestionAnswer

class ProgrammingQuestionAdmin(nested_admin.NestedModelAdmin):
    inlines = [AnswerInline]

class ProgrammingQuestionInline(nested_admin.NestedStackedInline):
    inlines=[AnswerInline]
    model = ProgrammingQuestion

class CodingQuestionInline(nested_admin.NestedStackedInline):
    model=CodingQuestion



admin.site.register(FacebookUser)
admin.site.register(CodingQuestion)
admin.site.register(CodingResult)
admin.site.register(BotUser)
admin.site.register(ProgrammingLanguage)
admin.site.register(ProgrammingQuestion, ProgrammingQuestionAdmin)
admin.site.register(ProgrammingQuestionAnswer)
admin.site.register(ProgrammingCategory)

