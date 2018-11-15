from .models import Notification
from blog.models import Post, User


def send(sender, recipient, verb, blog_id):
    notification = Notification(
        sender=sender,
        recipient=recipient,
        verb=verb,
        blog_id=blog_id)
    notification.save(notification)


def recieve(receiver, sender=None):
    notification = []
    if sender:
        return Notification.objects.filter(
            receiver=receiver,
            sender=sender
        ).order_by('-timestamp')
    else:
        q = Notification.objects.filter(
            object_id=receiver.id
        ).order_by('-timestamp')
        for i in q:
            o = {
                'verb': i,
                'user': User.objects.filter(id=i.sender_id),
                'blog': Post.objects.get(id=i.blog_id)
            }
            notification.append(o)
        unread_count = 0
        for i in q:
            if i.unread:
                unread_count += 1
        return notification, unread_count
