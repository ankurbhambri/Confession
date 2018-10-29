from .models import Notification


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
        return Notification.objects.filter(
            object_id=receiver.id
        ).order_by('-timestamp')
