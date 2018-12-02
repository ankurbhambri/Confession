from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
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
    API to list all the approved blogs.<br>

        endpoints: /api/blogs
        Method: GET
        Returns:
            List of all Approved Blogs
    '''
    permission_classes = (permissions.AllowAny,)

    queryset = Post.objects.filter(is_approve=True)
    serializer_class = BlogSerializer


class CreateBlogView(viewsets.ModelViewSet):
    '''
    API to create a new blog.

        endpoints: /api/create-blog
        Method: POST
        * Login required
        Args:
            title: title of blog
            text:  text/content of blog
        Returns:
            title: title of blog
            text:  text/content of blog
            owner_id: owner id of blog
            request_from: api or tempalte(defaults: api)
    '''

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogCreateSerializer

    def create(self, request):
        try:
            request_data = request.data
            auth_keyword, token = get_authorization_header(request).split()
            user = JWT_DECODE_HANDLER(token).get('user_id', None)
            request_data['owner_id'] = user
            request_data['request_from'] = 'api'
            user = User.objects.get(id=user)
            serializer = BlogCreateSerializer(data=request_data)
            if serializer.is_valid():
                post = serializer.save()
                if post:
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
    API to show list of blogs of current user.

        endpoints: /api/myblog
        Method: GET
        * Login required
        Returns:
            List of all blogs of current user.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogSerializer

    def get_queryset(self):
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        return Post.objects.filter(owner_id=user, is_approve=True)


class PostDetailView(viewsets.ModelViewSet):
    '''
    API to perform different actions on given blog.

        endpoints: /api/blog/<int:pk>
        * Login required
    '''

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogCreateSerializer
    queryset = Post.objects.all()

    def retrieve(self, request, pk=None):
        '''
        Retrieve non deleted blog by default.
        **deleted = 1** to retrieve deleted blog.

            Method: GET
            Args:
                deleted: (optional: default 0)1 or 0
            Returns:
                full blog related response.
        '''
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
        '''
        Update the updated blog.

            Method: PUT
            Args:
                title: title of blog
                text:  text/content of blog
            Returns:
                full blog related response.
        '''
        request_data = request.data
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        user = User.objects.get(id=user)
        # q = Post.objects.filter(owner_id=user, is_deleted=False)
        # queryset = get_object_or_404(q, pk=pk)

        request_data['owner_id'] = user.id
        # request_data['request_from'] = 'api'
        serializer = BlogCreateSerializer(data=request_data)
        if serializer.is_valid():
            post = serializer.save()
            if post:
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {"success": False, "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        # # Update the blog
        # is_updated = Post.objects.filter(
        #     owner_id=user, pk=pk).update(**request.data)
        # if is_updated:
        #     serializer = BlogSerializer(queryset)
        #     return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Delete blog of given blog id.

            Method: DELETE
            Returns:
                username: current user
                success: success status
        '''
        auth_keyword, token = get_authorization_header(self.request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        user = User.objects.get(id=user)
        try:
            Post.objects.get(owner_id=user, pk=pk, is_deleted=False).delete()
            data = {
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

        endpoints: /api/approval-list
        Method: GET
        * Login required
        Args:
            is_approve: (optional)Boolean
                - True: For all approved blogs
                - False: For all non-approved blogs
        Returns:
            List of all Approved Blogs
    '''
    permission_classes = (
        permissions.IsAuthenticated,
        ChiefRequiredPermission,
    )
    serializer_class = BlogSerializer

    def get_queryset(self):
        approve_flag = True if self.request.GET.get(
            'is_approve', False) == 'true' else False
        return Post.objects.filter(is_approve=approve_flag)


class PostApprovalFormView(viewsets.ModelViewSet):
    '''
    API to approve blog by moderator.

        endpoints: /api/approve/<int:pk>
        Method: PUT
        * Login required
        Args:
            is_approve: Boolean
                - True: To approve blog
                - False: To unapprove blog
        Returns:
            username: current user
            success: success http_status
    '''
    permission_classes = (
        permissions.IsAuthenticated,
        ChiefRequiredPermission,
    )

    serializer_class = PostApprovalFormSerializer
    queryset = Post.objects.all()

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
            return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)


class CommentView(viewsets.ModelViewSet):
    '''
    API to comment on blog

        endpoints: /api/comment
        Method: POST
        * Login required
        Args:
            comment: Comment
            blog_id: blog id on which comment will apply
        Returns:
            username: current user
            success: success status
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer

    def create(self, request):
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
                        # 'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
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


class ReplyView(viewsets.ModelViewSet):
    '''
    API to reply on comment

        endpoints: /api/reply
        Method: POST
        * Login required
        Args:
            reply: Reply
            which_comment_id: comment id on which reply will apply
            blog_id: blog id on which comment will apply
        Returns:
            username: current user
            success: success status
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReplySerializer

    def create(self, request):
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
                        # 'token': JWT_ENCODE_HANDLER(JWT_PAYLOAD_HANDLER(user)),
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
    '''
    API to perform different actions on given blog.

        endpoints: /api/notification
        * Login required

        - retrieve: retrive notification of current user
            Method: GET
            Returns:
                List of all notification related response.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(object_id=self.request.user.id)

    def update(self, request, pk=None):
        '''
        API to change read status.

            - update: notification marked as read
                Method: PUT
                Args:
                    {} => blank json
                Returns:
                    success: Boolean
        '''
        Notification.objects.filter(
            object_id=request.user.id).update(unread=False)
        return Response({'success': True, }, status=status.HTTP_202_ACCEPTED)
