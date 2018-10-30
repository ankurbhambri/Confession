from .models import Notification
from blog.models import Post


def send(sender, recipient, verb):
    notification = Notification(
        sender=sender,
        recipient=recipient,
        verb=verb)
    notification.save(notification)


def recieve(receiver, sender=None):
    if sender:
        return Notification.objects.filter(
            receiver=receiver,
            sender=sender
        ).order_by('-timestamp')
    else:
        q = Notification.objects.filter(
            object_id=receiver.id
        ).order_by('-timestamp')
        unread_count = 0
        for i in q:
            if i.unread:
                unread_count += 1
        return q, unread_count
