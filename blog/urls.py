from django.urls import path
from django.contrib.auth import views
from .views import *


urlpatterns = [
    path('post', IndexView.as_view(), name='post'),
    path('post_list', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),

    path('', HomeView.as_view(), name="home"),
    path('post-approval-list/<int:pk>', PostApprovalView.as_view(), name='post_approval_list'),
]
