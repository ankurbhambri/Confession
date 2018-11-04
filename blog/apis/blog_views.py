from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework.authentication import get_authorization_header

from blog.models import Post, User
from notifications.models import Notification
from .serializers import *
from .permissions import ChiefRequiredPermission

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER


class HomeView(viewsets.ModelViewSet):
    '''
        API to list all the approved blogs
    '''
    permission_classes = (permissions.AllowAny,)

    queryset = Post.objects.filter(is_approve=True)
    serializer_class = BlogSerializer


class CreateBlogView(APIView):
    '''
        API to create a new blog
    '''

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            auth_keyword, token = get_authorization_header(request).split()
            user = JWT_DECODE_HANDLER(token).get('user_id', None)
            data['owner_id'] = user
            user = User.objects.get(id=user)
            serializer = BlogCreateSerializer(data=data)
            if serializer.is_valid():
                post = serializer.save()
                if post:
                    data = {
                        'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
                        'username': JWT_DECODE_HANDLER(token).get('username'),
                        'success': True
                    }
                    serializer = TokenSerializer(data=data)
                    if serializer.is_valid():
                        return Response(
                            serializer.data,
                            status=status.HTTP_201_CREATED
                        )
            else:
                return Response(
                    {"success": False, "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PostListView(viewsets.ModelViewSet):
    '''
        API to show list of blogs of loggedIn user
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogSerializer

    def get_queryset(self):
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        return Post.objects.filter(owner_id=user, is_approve=True)


class PostDetailView(viewsets.ViewSet):
    '''
        API for multiple uses described as follows:
          - retrieve(GET): retrive selected blog
          - update(PUT): update selected blog
          - destroy(DELETE): delete selected blog.
    '''

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogSerializer
    queryset = Post.objects.all()

    def retrieve(self, request, pk=None):
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        try:
            delete_flag = request.GET['deleted']
            if delete_flag == '1':
                flag = True
            else:
                flag = False
        except KeyError:
            flag = False
        q = Post.objects.filter(owner_id=user, is_deleted=flag)
        queryset = get_object_or_404(q, pk=pk)
        serializer = BlogSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        user = User.objects.get(id=user)
        Post.objects.filter(owner_id=user, pk=pk).update(**request.data)
        data = {
            'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
            'username': JWT_DECODE_HANDLER(token).get('username'),
            'success': True
        }
        serializer = TokenSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(data)

    def destroy(self, request, pk=None):
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        user = User.objects.get(id=user)
        try:
            Post.objects.get(owner_id=user, pk=pk, is_deleted=False).delete()
            data = {
                'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
                'username': JWT_DECODE_HANDLER(token).get('username'),
                'success': True
            }
            http_status = status.HTTP_202_ACCEPTED
        except ObjectDoesNotExist:
            data = {
                "username": JWT_DECODE_HANDLER(token).get('username'),
                'success': False,
            }
            http_status = status.HTTP_404_NOT_FOUND
        serializer = TokenSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, http_status)
        else:
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)


class PostApprovalListView(viewsets.ModelViewSet):
    '''
    API to list of all post that need to be approved or allready approved.
    is_approve = True/False
    '''
    permission_classes = (
        permissions.IsAuthenticated,
        ChiefRequiredPermission,
    )
    serializer_class = BlogSerializer

    def get_queryset(self):
        approve_flag = True if self.request.GET.get('is_approve', False) == 'true' else False
        return Post.objects.filter(is_approve=approve_flag)


class PostApprovalFormView(viewsets.ModelViewSet):
    '''
        API to approve the blog.
    '''
    permission_classes = (
        permissions.IsAuthenticated,
        ChiefRequiredPermission,
    )

    def update(self, request, pk=None):
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        try:
            approve_flag = request.data.get('is_approve', False)
            user = User.objects.get(id=user)
            post = Post.objects.get(pk=pk, is_deleted=False)
            post.is_approve = approve_flag
            post.save()
            data = {
                'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
                'username': JWT_DECODE_HANDLER(token).get('username'),
                'success': True
            }
            http_status = status.HTTP_202_ACCEPTED
        except ObjectDoesNotExist:
            data = {
                "username": JWT_DECODE_HANDLER(token).get('username'),
                'success': False,
            }
            http_status = status.HTTP_404_NOT_FOUND
        serializer = TokenSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, http_status)
        else:
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)


class CommentView(APIView):
    '''
    API to comment to blog
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            auth_keyword, token = get_authorization_header(request).split()
            user = JWT_DECODE_HANDLER(token).get('user_id', None)
            data['user_id'] = user
            user = User.objects.get(id=user)
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                comment = serializer.save()
                if comment:
                    data = {
                        'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
                        'username': JWT_DECODE_HANDLER(token).get('username'),
                        'success': True
                    }
                    serializer = TokenSerializer(data=data)
                    if serializer.is_valid():
                        return Response(
                            serializer.data,
                            status=status.HTTP_201_CREATED
                        )
            else:
                return Response(
                    {"success": False, "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReplyView(APIView):
    '''
    API to reply to comment
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            auth_keyword, token = get_authorization_header(request).split()
            user = JWT_DECODE_HANDLER(token).get('user_id', None)
            data['user_id'] = user
            user = User.objects.get(id=user)
            serializer = ReplySerializer(data=data)
            if serializer.is_valid():
                reply = serializer.save()
                if reply:
                    data = {
                        'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
                        'username': JWT_DECODE_HANDLER(token).get('username'),
                        'success': True
                    }
                    serializer = TokenSerializer(data=data)
                    if serializer.is_valid():
                        return Response(
                            serializer.data,
                            status=status.HTTP_201_CREATED
                        )
            else:
                return Response(
                    {"success": False, "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class NotificationView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(object_id=self.request.user.id)

    def update(self, request, pk=None):
        Notification.objects.filter(
            object_id=request.user.id).update(unread=False)
        return Response({'success': True, }, status=status.HTTP_202_ACCEPTED)
