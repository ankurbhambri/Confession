from django.urls import path
from rest_framework.documentation import include_docs_urls

from .account_views import (RegisterationView, LoginView)
from .blog_views import (
    HomeView,
    CreateBlogView,
    PostListView,
    PostDetailView,
    PostApprovalListView,
    PostApprovalFormView,
    CommentView,
    ReplyView,
    NotificationView,
)


post_detail = PostDetailView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'

})
post_list = PostListView.as_view({'get': 'list'})
post_approval_list = PostApprovalListView.as_view({'get': 'list'})

post_approve = PostApprovalFormView.as_view({'put': 'update'})
notification = NotificationView.as_view({
    'get': 'list',
    'put': 'update'
})

urlpatterns = [
    path('docs', include_docs_urls(
        title='Blogs API Docs'
    )),
    path('register', RegisterationView.as_view(), name='api-register'),
    path('login', LoginView.as_view(), name='api-login'),

    path('blogs', HomeView.as_view({'get': 'list'}), name='api-home'),
    path('create-blog', CreateBlogView.as_view({'post': 'create'}), name='api-create-blog'),
    path('myblog', post_list, name='api-myblog'),
    path(
        'blog/<int:pk>',
        post_detail,
        name='api-blog-operation'
    ),
    path('approval-list', post_approval_list, name='api-approval-list'),
    path('approve/<int:pk>', post_approve, name='api-approve'),

    path('comment', CommentView.as_view(), name='api-comment'),
    path('reply', ReplyView.as_view(), name='api-reply'),
    path('notification', notification, name='api-notification'),
]
