from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.conf import settings


# class ActivityType(models.Model):
#     activity_type = 


class Notification(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    recipient = GenericForeignKey('content_type', 'object_id')
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    unread = models.BooleanField(default=True, blank=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        app_label = 'notifications'

    def __str__(self):
        return self.verb

    def delete(self):
        self.deleted = True
        self.save()

    # def mark_as_read(self):
    #     if self.unread:
    #         self.unread = False
    #         self.save()

    # def mark_as_unread(self):
    #     if not self.unread:
    #         self.unread = True
    #         self.save()
