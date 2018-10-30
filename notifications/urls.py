from django.urls import path
from .views import notify_read_unread_view

urlpatterns = [
    path('notify_status', notify_read_unread_view, name='notify-status'),
]
