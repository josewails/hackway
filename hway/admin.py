from django.contrib import admin
from django import forms
import nested_admin
from ckeditor.widgets import  CKEditorWidget
from ckeditor_uploader.widgets import  CKEditorUploadingWidget
from .models import  (FacebookUser,
                      CodingQuestion,
                      CodingResult,
                      BotUser,
                      ProgrammingLanguage,
                      ProgrammingQuestion,
                      ProgrammingQuestionAnswer,
                      ProgrammingCategory,
                      Course,
                      CourseSegment)



class AnswerInline(nested_admin.NestedTabularInline):
    model = ProgrammingQuestionAnswer

class ProgrammingQuestionAdmin(nested_admin.NestedModelAdmin):
    exclude = ['course_segment']
    inlines = [AnswerInline]

class ProgrammingQuestionInline(nested_admin.NestedStackedInline):
    inlines=[AnswerInline]
    model = ProgrammingQuestion

class CodingQuestionInline(nested_admin.NestedStackedInline):
    model=CodingQuestion

class CourseSegmentAdminForm(forms.ModelForm):
    body=forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model=CourseSegment
        fields=['title', 'course']


class CourseSegmentAdmin(nested_admin.NestedModelAdmin):
    form = CourseSegmentAdminForm
    inlines=[ProgrammingQuestionInline, CodingQuestionInline]


admin.site.register(FacebookUser)
admin.site.register(CodingQuestion)
admin.site.register(CodingResult)
admin.site.register(BotUser)
admin.site.register(ProgrammingLanguage)
admin.site.register(ProgrammingQuestion, ProgrammingQuestionAdmin)
admin.site.register(ProgrammingQuestionAnswer)
admin.site.register(ProgrammingCategory)
admin.site.register(Course)
admin.site.register(CourseSegment, CourseSegmentAdmin)
