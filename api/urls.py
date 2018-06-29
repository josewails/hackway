from django.urls import path
from rest_framework.authtoken import views as rest_views

from .views import (
    FaceBookUserCreateAPIView,
    FacebookUserListAPIView,
    FacebookUserRetrieveAPIView,
    FacebookUserUpdateAPIView,
    FacebookUserDeleteAPIView,
    CodingQuestionCreate,
    CodingQuestionListAPIView,
    CodingQuestionRetrieveAPIView,
    CodingQuestionUpdateAPIView,
    CodingQuestionDifficultyList,
    CheckCode,
    RetrieveResults,
    GetAllRankings,
    GetIndividualRanking,
    FacebookUserCodingResultList,
    ProgrammingLanguagesList,
    CheckGroundCode,
    ProgrammingQuestionExplanation
)


urlpatterns = [
    path('generate_auth_token', rest_views.obtain_auth_token),
    path('facebook_users/create', FaceBookUserCreateAPIView.as_view(), name='create_facebook_user'),
    path('facebook_users', FacebookUserListAPIView.as_view(),name='facebook_users_list' ),
    path('facebook_users/<facebook_id>', FacebookUserRetrieveAPIView.as_view()),
    path('facebook_users/<facebook_id>/update', FacebookUserUpdateAPIView.as_view(), name='update_facebook_user'),
    path('facebook_users/<facebook_id>/delete', FacebookUserDeleteAPIView.as_view()),
    path('coding_questions/create', CodingQuestionCreate.as_view(), name='create_coding_question'),
    path('coding_questions', CodingQuestionListAPIView.as_view(), name='all_coding_questions'),
    path('coding_questions/<id>', CodingQuestionRetrieveAPIView.as_view()),
    path('coding_questions/<id>/update', CodingQuestionUpdateAPIView.as_view()),
    path('coding_questions/difficulty_level/<difficulty_level>', CodingQuestionDifficultyList.as_view()),
    path('check_code', CheckCode.as_view()),
    path('retrieve_results', RetrieveResults.as_view()),
    path('get_all_rankings', GetAllRankings.as_view()),
    path('get_individual_ranking', GetIndividualRanking.as_view()),
    path('coding_results/<facebook_id>', FacebookUserCodingResultList.as_view()),
    path('programming_questions', ProgrammingLanguagesList.as_view(), name='all_programming_languages'),
    path('programming_question_explanation', ProgrammingQuestionExplanation.as_view()),
    path('check_ground_code', CheckGroundCode.as_view())
]