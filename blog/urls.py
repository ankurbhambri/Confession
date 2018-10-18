from django.urls import path
from django.conf.urls import url
from .views import *


urlpatterns = [
    path(
        'post',
        IndexView.as_view(),
        name='post'
    ),
    path(
        'post_list',
        PostListView.as_view(),
        name='post_list'
    ),
    path(
        'post/<int:pk>',
        PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'post/<int:pk>/update',
        PostUpdateView.as_view(),
        name='post_update'
    ),
    path(
        '',
        HomeView.as_view(),
        name="home"
    ),
    path(
        'post-approval-list/<int:pk>',
        PostApprovalView.as_view(),
        name='post_approval_list'
    ),
    path(
        'post/approve-list',
        PostApprovalListView.as_view(),
        name="post_approve_list"
    ),
    path(
        'post/<int:pk>/delete',
        PostDeleteView.as_view(),
        name="post_delete"
    ),
    url(
        r'post/comment/(?P<pk>[0-9]+)$',
        CommentReplyView.as_view(),
        name="comment_reply"
    ),
    # path(
    #     'post/comment/<int:pk>',
    #     CommentReplyView.as_view(),
    #     name="comment_reply"
    # ),
]
