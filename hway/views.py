from .utils import(
    get_individual_score,
    get_score,
    validate_code,
    generate_api_key,
    validate_ground_code)

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
    )
from .models import (
    FacebookUser,
    CodingQuestion,
    CodingResult,
    ProgrammingLanguage,
    BotUser,
    ProgrammingQuestion,
    Course,
    CourseSegment
    )
from .serializers import (
    FacebookUserSerializer,
    CodingQuestionSerializer,
    CodingResultSerializer,
    CodingQuestionCreateSerializer,
    ProgrammingLanguageSerializer,
    ProgrammingQuestionExplanationSerializer
    )
from rest_framework.views import APIView
from rest_framework.response import Response
import json, requests,logging


languages={
    'python': 30,
    'java': 3,
    'javascript': 20
}
logger = logging.getLogger(__name__)

class FaceBookUserCreateAPIView(APIView):

    """
    View to create a new facebook user
    """

    def post(self,request, format=None):

        """

        :param request: The received request
        :param format: None
            -> Extracts data from the request and tries to create a new facebook user

        :return: success if the facebook user is created successfully
        """

        name = request.POST.get('name', None)
        facebook_id = request.POST.get('facebook_id', None)
        email = request.POST.get('email',None)
        profile_picture_url = request.POST.get('profile_picture_url', None)
        private_api_key = request.POST.get('private_api_key', None)


        if name and facebook_id:
            try:
                facebook_user = FacebookUser.objects.create(
                    name=name,
                    facebook_id=facebook_id,
                    email=email,
                    profile_picture_url=profile_picture_url,
                    private_api_key = private_api_key
                )
                facebook_user.save()
                data = {
                    'success': 'object created successfully'
                }

            except:
                try:
                    current_facebook_user = FacebookUser.objects.get(facebook_id=facebook_id)
                except:
                    data = {
                        'error': 'An error occured trying to create that facebook user'
                    }

                    return Response(data)

                current_facebook_user.email = email,
                current_facebook_user.name = name
                current_facebook_user.profile_picture_url = profile_picture_url
                current_facebook_user.private_api_key = private_api_key
                current_facebook_user.save()

                data = {
                    'success': 'Profile updated successfully'
                }

            return Response(data)
        else:
            data = {
                'error': 'An error occured trying to create that facebook user'
            }
            return Response(data)


class FacebookUserListAPIView(ListAPIView):
    """View to return all facebook users"""

    serializer_class = FacebookUserSerializer
    queryset =  FacebookUser.objects.all()

class FacebookUserRetrieveAPIView(RetrieveAPIView):
    """View to retrieve a give facebook user"""

    serializer_class = FacebookUserSerializer
    queryset = FacebookUser.objects.all()
    lookup_field = 'facebook_id'

class FacebookUserUpdateAPIView(UpdateAPIView):
    """View to update a given facebook user"""

    serializer_class = FacebookUserSerializer
    queryset = FacebookUser.objects.all()
    lookup_field = 'facebook_id'

class FacebookUserDeleteAPIView(DestroyAPIView):
    """View to delete a given facebook user"""

    serializer_class = FacebookUserSerializer
    queryset = FacebookUser.objects.all()
    lookup_field = 'facebook_id'


class CodingQuestionCreate(APIView):
    """View to create a new coding Question"""

    serializer_class = CodingQuestionCreateSerializer

    def post(self,request,format=None):
        """

        :param request: The post request received by API
        :param format: None
        :return: success if the coding question is created successfully and false otherwise
        """

        difficulty_level_choices=['simple', 'intermediate', 'difficult']
        language_choices=['5', '30']

        try:
            api_key = request.POST['api_key']
        except:
            api_key = None


        if api_key:
            try:
                current_facebook_user=FacebookUser.objects.get(private_api_key=api_key)
            except KeyError:
                data = {
                    'error': 'That api key is invalid'
                }

                return Response(data)
        else:
            data = {
                'error': 'The request must contain api_key field'
            }

            return Response(data)

        try:
            title=request.POST['title']
        except:
            data = {
                'error': 'The request must contain title field'
            }

            return Response(data)

        try:
            question=request.POST['question']
        except:
            data = {
                'error': 'The request must contain question field'
            }

            return Response(data)


        try:
            difficulty_level=request.POST['difficulty_level']
        except:
            difficulty_level=None

        if difficulty_level:
            if difficulty_level not in difficulty_level_choices:
                data = {
                    'error': 'difficulty_level is in invalid'
                }

                return Response(data)
        else:
            data = {
                'error': 'The request must contain api_key field'
            }

            return Response(data)

        try:
            sample_input=request.POST['sample_input']
        except:
            sample_input=None

        if sample_input:
            if type(json.loads(sample_input)) != list:

                data={
                    'error': 'sample_input must be of type list'
                }

                return Response(data)

        else:
            data = {
                'error': 'The request must contain sample_input field'
            }

            return Response(data)

        try:
            sample_output=request.POST['sample_output']
        except:
            sample_output=None

        if sample_output:
            if type(json.loads(sample_output)) != list:
                data={
                    'error': 'sample_output must be of type list'
                }

                return Response(data)
        else:
            data = {
                'error': 'The request must contain sample_output field'
            }

            return Response(data)

        try:
            solution_language=request.POST['solution_language']
        except:
            solution_language=None

        if solution_language:
            if solution_language not in language_choices:
                data = {
                    'error': 'The solution_language is invalid'
                }
                return Response(data)
        else:
            data = {
                'error': 'The request must contain solution field'
            }

            return Response(data)

        try:
            input=request.POST['input']
        except:
            input=None

        if input:
            if type(json.loads(input)) != list:
                data = {
                    'error': 'Input must be of type list'
                }

                return Response(data)
        else:
            data = {
                'error': 'The request must contain input field'
            }

            return Response(data)

        try:
            solution = request.POST['solution']
        except:
            solution = None


        if solution:
            solution_data = {
                'api_key': 'hackerrank|394048-2076|cbdd81cef0663eb85cd43e24355f42b1efa2e2a8',
                'source': solution,
                'lang': int(solution_language),
                'testcases': input,
                'format': 'JSON'
            }

            url = 'http://api.hackerrank.com/checker/submission.json'

            solution_output=requests.post(url=url , data=solution_data).json()

            if solution_output['result']['compilemessage']:
                data={
                    'error': 'Your solution did not compile',
                    'compilemessage': solution_output['result']['compilemessage']
                }

                return Response(data)
        else:
            data = {
                'error': 'The request must contain solution field'
            }

            return Response(data)

        new_question=CodingQuestion(
            author=current_facebook_user,
            title=title,
            question=question,
            solution=solution,
            solution_language=solution_language,
            sample_input=sample_input,
            sample_output=sample_output,
            difficulty_level=difficulty_level,
            input=input
        )



        new_question.save()
        data={
            'success': 'Your question was saved successfully'
        }

        return Response(data)


class CodingQuestionListAPIView(ListAPIView):
    """
    Returns a list of all CodingQuestions
    """
    serializer_class = CodingQuestionSerializer
    queryset =  CodingQuestion.objects.all()

class CodingQuestionDifficultyList(ListAPIView):

    """
    Returns a list of all coding question with a given difficulty level
    """

    serializer_class = CodingQuestionSerializer

    def get_queryset(self):
        difficulty_level=self.kwargs['difficulty_level']
        return CodingQuestion.objects.filter(difficulty_level=difficulty_level)

class CodingQuestionRetrieveAPIView(RetrieveAPIView):

    """
    Returns the details of a specific CodingQuestion
    """
    serializer_class=CodingQuestionSerializer
    queryset = CodingQuestion.objects.all()
    lookup_field =  'id'

class CodingQuestionUpdateAPIView(UpdateAPIView):
    """
    Updates the details of a given Coding Question
    """
    serializer_class = CodingQuestionCreateSerializer
    queryset = FacebookUser.objects.all()
    lookup_field = 'id'


class FacebookUserCodingResultList(ListAPIView):

    """
    Returns a list of coding results for a given facebook user
    """

    serializer_class = CodingResultSerializer

    def get_queryset(self):
        facebook_id=self.kwargs['facebook_id']
        return CodingResult.objects.filter(coder_facebook_id=facebook_id)



class ProgrammingLanguagesList(ListAPIView):
    """
    Returns a list of all ProgrammingQuestions
    """
    serializer_class = ProgrammingLanguageSerializer
    queryset = ProgrammingLanguage.objects.all()

class GetIndividualRanking(APIView):

    """
    Gets the ranking of a specific user using their facebook_id and messenger_id
    """

    def post(self, request, format=None):

        facebook_id=request.POST['facebook_id']
        messenger_id=request.POST['messenger_id']

        data=get_individual_score(facebook_id=facebook_id, messenger_id=messenger_id)

        return Response(data)

class GetAllRankings(APIView):

    def get(self, request, format=None):
        all_bot_users=BotUser.objects.all()
        all_rankings=[]

        for bot_user  in all_bot_users:
            if bot_user.facebook_user:
                messenger_id = bot_user.messenger_id
                facebook_id = bot_user.facebook_user.facebook_id

                ranking = get_individual_score(facebook_id=facebook_id, messenger_id=messenger_id)

                data = {
                    'name': bot_user.facebook_user.name,
                    'ranking': ranking
                }

                all_rankings.append(data)

        all_rankings=sorted(all_rankings, key=lambda ranking: ranking['ranking']['overall_score'])

        return Response(all_rankings)


class  RetrieveResults(APIView):

    def post(self, request, format=None):
        try:
            facebook_id = request.POST['facebook_id']
        except:
            facebook_id = None

        try:
            question_id = request.POST['question_id']
        except:
            question_id = None

        if facebook_id and question_id:
            try:
                current_result=CodingResult.objects.get(coder_facebook_id=facebook_id, question_solved_id=question_id)
            except:
                current_result=None

            if current_result:
                try:
                    current_question=CodingQuestion.objects.get(id=question_id)
                except:
                    current_question=None

                if current_question:
                    testcase_index=current_result.last_testcase_passed_index
                    testcases=json.loads(current_question.input)
                    possible_score=len(testcases)*get_score(current_question.difficulty_level)

                    scores = json.loads(current_result.scores)
                    score = round((scores[-1]/ possible_score), 4)*100

                    if len(testcases)==testcase_index:

                        data= {
                            'success': True,
                            'question': current_question.question,
                            'question_title': current_question.title,
                            'test_cases_passed': testcases[:testcase_index],
                            'source_code': current_result.coder_source_code,
                            'score': score

                        }

                        return Response(data)

                    else:
                        data={
                            'success': False,
                            'question': current_question.question,
                            'question_title': current_question.title,
                            'testcases_passed': testcases[:testcase_index],
                            'testcases_failed': testcases[testcase_index:],
                            'source_code': current_result.coder_source_code,
                            'error': current_result.error,
                            'score': score
                        }
                        return Response(data)
                else:
                    data={
                        'error': 'Looks like that coding problem does not exist'
                    }

                    return Response(data)

            else:
                data={
                    'error': 'we could not retrieve the requested resource'
                }

                return Response(data)
        else:
            data = {
                'error': 'We could not retrieve the requested resouce'
            }

            return Response(data)


class CheckCode(APIView):

    def post(self, request, format=None):
        try:
            question_id=request.POST['question_id']
        except:
            question_id=None

        try:
            source_code=request.POST['source_code']
        except:
            source_code=None

        try:
            facebook_id=request.POST['facebook_id']
        except:
            facebook_id=None

        try:
            language_used=languages[request.POST['language_used']]
        except:
            language_used=None

        if question_id and source_code and language_used:
            data=validate_code(source_code, question_id, language_used, facebook_id)

        else:
            data={
                'error': 'There were were some errors in the post request'
            }

        return Response(data)

class GetAPIKey(APIView):

    def post(self, request,format=None):
        try:
            facebook_id=request.POST['facebook_id']
        except:
            facebook_id=None

        if facebook_id:
            try:
                current_facebook_user = FacebookUser.objects.get(facebook_id=facebook_id)
            except:
               current_facebook_user=None

            if current_facebook_user:
                api_key=generate_api_key(32)
                current_facebook_user.public_api_key=api_key
                current_facebook_user.save()

                data={
                    'api_key': api_key
                }

                return Response(data)
            else:
                data={
                    'error': 'User with that facebook id does not exist'
                }

                return Response(data)

        else:
            data={
                'error': 'There was an error in the request'
            }

            return Response(data)
class ProgrammingQuestionExplanation(APIView):
    serializer_class=ProgrammingQuestionExplanationSerializer

    def post(self, request, format=None):
        try:
            question_id=request.POST['question_id']
        except:
            question_id=None

        if question_id:
            try:
                current_question=ProgrammingQuestion.objects.get(id=question_id)
            except:
                data={
                    'error': 'We could not retrieve the question with that id'
                }

                return Response(data)

            if current_question.explanation:
                data={
                    'explanation': current_question.explanation
                }

            else:
                data={
                    'explanation': 'The explanation for this question is yet to be added'
                }

            return Response(data)

        else:
            data={
                'error': 'question_id is a required field'
            }

            return Response(data)

#View to validate code from the coding ground
class CheckGroundCode(APIView):

    def post(self, request, format=None):
        try:
            source=request.POST['source_code']
        except:
            source=None

        try:
            language_used=request.POST['language_used']
        except:
            language_used=None

        try:
            testcases=request.POST['testcases']
        except:
            testcases=None


        if source and language_used and testcases:
            data=validate_ground_code(source, languages[language_used], testcases)
            return Response(data)
        else:
            data={
                'error': 'There was an error with that request'
            }
            if not source:
                data={
                    'error': 'The request must contain source_code field'
                }

            if not  language_used:
                data={
                    'error': 'The request must contain a language_used field'
                }

            if not testcases:
                data={
                    'error': 'The request must contain the testcases field'
                }

            return Response(data)

class GetAllCourses(APIView):

    def get(self, request, format=None):
        all_courses=Course.objects.all()
        courses=[]
        for course in all_courses:
            courses.append({
                'name': course.name,
                'description': course.description
            })
        data={
            'courses': courses
        }

        return Response(data)


class CourseDetails(APIView):
    def post(self, request, format=None):
        try:
            course_id = request.POST['course_id']
        except:
            data={
                'error': 'The request must have a course_id field'
            }

            return Response(data)
        try:
            current_course=Course.objects.get(id=course_id)
        except:
            current_course=None

        if current_course:
            data={}
            data['name']=current_course.name
            data['description']=current_course.description

            all_course_segments=current_course.course_segments.order_by('id')
            course_segments=[]
            for course_segment in all_course_segments:
                course_segments.append({
                    'title': course_segment.title,
                    'intro': course_segment.intro
                })

            data['course_segments']=course_segments

            return Response(data)
        else:
            data={
                'error': 'We could not retrieve the requested resource'
            }

            return Response(data)

class CourseSegmentDetails(APIView):

    def post(self, request, format=None):

        try:
            segment_id = request.POST['segment_id']
        except:
            data={
                'Error' : 'The request must contain segment_id'
            }
            return Response(data)

        try:
            current_course_segment = CourseSegment.objects.get(id=segment_id)
        except:
            data={
                'Error': 'We could not retrieve the request resource'
            }

            return Response(data)

        data={}
        data['title']=current_course_segment.title
        data['intro']=current_course_segment.intro
        data['body']=current_course_segment.body

        return Response(data)









