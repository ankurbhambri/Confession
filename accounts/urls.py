from django.views.generic import TemplateView
from django.urls import path, include
from django.conf.urls import url
from .views import *


urlpatterns = [
    # path('api/', include('blog.apis.urls')),
    path(
        'user-info/',
        UserInfoView.as_view(),
        name="user_info"
    ),
    url(
        r'user-detail/(?P<slug>[\w.@+-]+)/$',
        UserDetailView.as_view(),
        name="user_detail"
    ),
    path(
        'greeting/',
        TemplateView.as_view(template_name="blog/greeting.html"),
        name='greeting'
    ),
    url(
        r'skill/(?P<slug>[\w.@+-]+)/$',
        SkillUpdateView.as_view(),
        name='skill'
    ),
    url(
        r'qualification/(?P<slug>[\w.@+-]+)/$',
        QualificationView.as_view(),
        name='qualification'
    ),
    url(
        r'experience/(?P<slug>[\w.@+-]+)/$',
        ExperienceView.as_view(),
        name='experience'
    ),
]
