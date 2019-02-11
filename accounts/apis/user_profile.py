from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.authentication import get_authorization_header

from .serializers import *
from accounts.models import *

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER


class CreateUserProfileView(viewsets.ViewSet):
    '''
    API to user profile.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TokenSerializer

    def update(self, request, pk=None):
        '''
        API to create user profile.

            endpoints: /api/user
            Method: POST
            * Login required
            Args:
                avatar: profile pic
                title:  title of profile
                aboutme: description/ about me
            Returns:
                username: current user
                success: success status
        '''
        try:
            request_data = request.data
            auth_keyword, token = get_authorization_header(request).split()
            user = JWT_DECODE_HANDLER(token).get('user_id', None)
            request_data['user_id'] = user
            is_updated = UserInfo.objects.filter(user_id=user).update(**request_data)
            if is_updated:
                data = {
                    "username": JWT_DECODE_HANDLER(token).get('username'),
                    'success': True,
                }
                serializer = TokenSerializer(data=data)
                if serializer.is_valid():
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"success": False, "error": "Not Updated"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class SkillView(viewsets.ModelViewSet):
    '''
    API for skills .
    '''

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SkillSerializer

    def retrieve(self, request, pk=None):
        '''
        Retrieve Skills of logedIn user.

            endpoints: /api/skill
            Method: GET
            * Login required
            Returns:
                Skills of logedIn user.
        '''
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        queryset = SkillSet.objects.filter(user_id=user)
        serializer = SkillSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        '''
        API to create skills

            endpoints: /api/skill
            Method: POST
            * Login required
            Args:
                List of dictionary haviing skill and rating with
                skill: skill name
                rating: rating from 0 to 100
            Returns:
                skill: given skill
                rating: given rating
                success: success status
        '''
        error = None
        stat = None
        try:
            request_data = request.data.get('data')
            auth_keyword, token = get_authorization_header(request).split()
            user = JWT_DECODE_HANDLER(token).get('user_id', None)
            user = User.objects.get(id=user)
            for data in request_data:
                data.update({'user_id': user.id})
            serializer = SkillSerializer(data=request_data, many=True)
            if serializer.is_valid():
                skill = serializer.save()
                if skill:
                    data = {
                        'success': True,
                        'username': user.username
                    }
                    serializer = TokenSerializer(data=data)
                    if serializer.is_valid():
                        data = serializer.data
                        stat = 200
                    else:
                        error = serializer.errors
                else:
                    error = 'Data Not Save'
            else:
                error = serializer.errors
        except Exception as e:
            error = str(e)
        finally:
            if stat:
                return Response(
                    data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"success": False, "error": error},
                    status=status.HTTP_400_BAD_REQUEST
                )

    def update(self, request, pk=None):
        request_data = request.data.get('data')
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        user = User.objects.get(id=user)
        for data in request_data:
            data.update({'user_id': user.id})
        total_update = []
        for data in request_data:
            serializer = SkillSerializer(data=request_data)
            if serializer.is_valid():
                post = serializer.save()
                if post:
                    total_update.append(post)
            else:
                total_update.append(serializer.errors)
        if append:
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class QualificationView(viewsets.ModelViewSet):
    '''
    API for qualification.
    '''

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QualificationSerializer

    def retrieve(self, request, pk=None):
        '''
        Retrieve Qualifications of logedIn user.

            endpoints: /api/qualification
            Method: POST
            * Login required
            Returns:
                List of dictionary having following keys:
                qualification: qualification name
                specialization: specialization in which field
                grade: Grade or Marks
                from_year: joining year of qualification
                completion_year: complition year
                achievement: Any achievement or project or awards.
        '''
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        queryset = Qualification.objects.filter(user_id=user)
        serializer = QualificationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        '''
        API to create qualifications.

            endpoints: /api/qualification
            Method: POST
            * Login required
            Args:
                qualification: qualification name
                specialization: specialization in which field
                grade: Grade or Marks
                from_year: joining year of qualification
                completion_year: complition year
                achievement: Any achievement or project or awards.
            Returns:
                username: username of logedIn user
                success: success status
        '''
        error = None
        stat = None
        try:
            request_data = request.data.get('data')
            auth_keyword, token = get_authorization_header(request).split()
            user = JWT_DECODE_HANDLER(token).get('user_id', None)
            for data in request_data:
                data.update({'user': user})
            serializer = QualificationSerializer(data=request_data, many=True)
            if serializer.is_valid():
                skill = serializer.save()
                if skill:
                    data = {
                        'success': True,
                        'username': User.objects.get(id=user).username
                    }
                    serializer = TokenSerializer(data=data)
                    if serializer.is_valid():
                        data = serializer.data
                        stat = 200
                    else:
                        error = serializer.errors
                else:
                    error = 'Data Not Save'
            else:
                error = serializer.errors
        except Exception as e:
            error = str(e)
        finally:
            if stat:
                return Response(
                    data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"success": False, "error": error},
                    status=status.HTTP_400_BAD_REQUEST
                )


class ExperienceView(viewsets.ModelViewSet):
    '''
    API for experience.
    '''

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ExperienceSerializer

    def retrieve(self, request, pk=None):
        '''
        Retrieve Experience of logedIn user.

            endpoints: /api/experience
            Method: GET
            Returns:
                List of dictionary having following keys:
                designation: Designation of employer
                org_name: organization name
                start_month: joining month
                start_year: joining year
                end_month: End month of employer
                completion_year: End year of employer
                present_working: True
                description: Description or any achievement or project desription
        '''
        # auth_keyword, token = get_authorization_header(self.request).split()
        # user = JWT_DECODE_HANDLER(token).get('user_id', None)
        queryset = Experience.objects.filter(user_id=pk)
        serializer = ExperienceSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None):
        '''
        API to create qualifications.

            endpoints: /api/qualification
            Method: POST
            * Login required
            Args:
                designation: Designation of employer
                org_name: organization name
                start_month: joining month
                start_year: joining year
                end_month: End month of employer
                completion_year: End year of employer
                present_working: True
                description: Description or any achievement or project desription
            Returns:
                username: username of logedIn user
                success: success status
        '''
        error = None
        stat = None
        try:
            request_data = request.data.get('data')
            auth_keyword, token = get_authorization_header(request).split()
            user = JWT_DECODE_HANDLER(token).get('user_id', None)
            for data in request_data:
                data.update({'user': user})
            if user == pk:
                serializer = ExperienceSerializer(data=request_data, many=True)
                if serializer.is_valid():
                    experience = serializer.save()
                    if experience:
                        data = {
                            'success': True,
                            'username': User.objects.get(id=user).username
                        }
                        serializer = TokenSerializer(data=data)
                        if serializer.is_valid():
                            data = serializer.data
                            stat = 200
                        else:
                            error = serializer.errors
                    else:
                        error = 'Data Not Save'
                else:
                    error = serializer.errors
            else:
                raise Exception("Login and called object are not same")
        except Exception as e:
            error = str(e)
        finally:
            if stat:
                return Response(
                    data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"success": False, "error": error},
                    status=status.HTTP_400_BAD_REQUEST
                )
