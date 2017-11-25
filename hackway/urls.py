"""devpulse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))


"""
from django.conf import settings

from django.conf.urls import url, include

from django.contrib import admin
from hway.views import (
    FaceBookUserCreateAPIView,
    FacebookUserListAPIView,
    FacebookUserRetrieveAPIView,
    FacebookUserUpdateAPIView,
    FacebookUserDeleteAPIView,
    CodingQuestionCreate,
    CodingQuestionListAPIView,
    CodingQuestionRetrieveAPIView,
    CodingQuestionUpdateAPIView,
    FacebookUserCodingResultList,
    CodingQuestionDifficultyList,
    ProgrammingQuestionsList,
    GetIndividualRanking,
    CheckCode,
    RetrieveResults,
    GetAllRankings,
    GetAPIKey,
    ProgrammingQuestionExplanation,
    CheckGroundCode,
    GetAllCourses,
    CourseDetails,
    CourseSegmentDetails
    )

from hway.hway_views import  (
    home
)

from hway.bot_views import (
    webhook,
    send_code_results
)

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^webhook$', webhook),
    url(r'^facebook_users/create$', FaceBookUserCreateAPIView.as_view(), name='create_facebook_user'),
    url(r'^facebook_users$', FacebookUserListAPIView.as_view(),name='facebook_users' ),
    url(r'^facebook_users/(?P<facebook_id>[\w]+)/$', FacebookUserRetrieveAPIView.as_view()),
    url(r'^facebook_users/(?P<facebook_id>[\w]+)/update$', FacebookUserUpdateAPIView.as_view()),
    url(r'^facebook_users/(?P<facebook_id>[\w]+)/delete$', FacebookUserDeleteAPIView.as_view()),
    url(r'^coding_questions/create$', CodingQuestionCreate.as_view()),
    url(r'^coding_questions$', CodingQuestionListAPIView.as_view()),
    url(r'^coding_questions/(?P<id>[\d]+)/$', CodingQuestionRetrieveAPIView.as_view()),
    url(r'^coding_questions/(?P<id>[\w]+)/update$', CodingQuestionUpdateAPIView.as_view()),
    url(r'^coding_questions/difficulty_level/(?P<difficulty_level>[\w]+)/$', CodingQuestionDifficultyList.as_view()),
    url(r'^check_code$', CheckCode.as_view()),
    url(r'^retrieve_results$', RetrieveResults.as_view()),
    url(r'^get_all_rankings$', GetAllRankings.as_view()),
    url(r'^get_individual_ranking$', GetIndividualRanking.as_view()),
    url(r'^coding_results/(?P<facebook_id>[\w]+)$', FacebookUserCodingResultList.as_view()),
    url(r'^send_coding_results$', send_code_results),
    url(r'^programming_questions$', ProgrammingQuestionsList.as_view()),
    url(r'^programming_questions$', ProgrammingQuestionsList.as_view()),
    url(r'^get_api_key$', GetAPIKey.as_view()),
    url(r'^programming_question_explanation$', ProgrammingQuestionExplanation.as_view()),
    url(r'^check_ground_code', CheckGroundCode.as_view()),
    url(r'^get_all_courses$', GetAllCourses.as_view()),
    url(r'^course_details$', CourseDetails.as_view()),
    url(r'^course_segment_details$', CourseSegmentDetails.as_view())
]



if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

