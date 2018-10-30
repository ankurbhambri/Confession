
from .models import Notification
from django.http import JsonResponse


def notify_read_unread_view(request):
    Notification.objects.filter(object_id=request.user.id).update(unread=False)
    return JsonResponse({'a': 100}, status=201)
