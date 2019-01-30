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


class CreateUserProfileView(viewsets.ModelViewSet):
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

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TokenSerializer

    def update(self, request, pk=None):
        try:
            request_data = request.data
            auth_keyword, token = get_authorization_header(request).split()
            user = JWT_DECODE_HANDLER(token).get('user_id', None)
            # user = User.objects.get(id=user)
            request_data['user_id'] = user
            is_updated = UserInfo.objects.filter(user_id=user).update(**request_data)
            if is_updated:
                # post = serializer.save()
                # if post:
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
    API to add skills .

        endpoints: /api/skill
        Method: POST
        * Login required
        Args:
            skill: skill name
            rating: rating from 0 to 100
        Returns:
            skill: given skill
            rating: given rating
            success: success status
    '''

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SkillSerializer

    def create(self, request):
        # try:
        request_data = request.data
        auth_keyword, token = get_authorization_header(request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        user = User.objects.get(id=user)
        request_data['user_id'] = user
        serializer = SkillSerializer(data=request_data)
        if serializer.is_valid():
            skill = serializer.save()
            if skill:
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {"success": False, "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        # except Exception as e:
        #     return Response(
        #         {"success": False, "error": str(e)},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
