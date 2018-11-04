from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


REQUEST_CHOICES = (
    ('api', 'api'),
    ('template', 'template')
)


class User(AbstractUser):
    is_editor = models.BooleanField(default=False)
    is_chief = models.BooleanField(default=False)


class Post(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=255)
    text = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now_add=True)
    is_approve = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    request_from = models.CharField(
        max_length=10,
        choices=REQUEST_CHOICES,
        default='template'
    )

    def __str__(self):
        return self.title

    def delete(self):
        self.is_deleted = True
        self.save()

    class Meta:
        ordering = ["-created_date"]


class Editor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return self.user


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_datetime']


class Reply(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reply'
    )
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    which_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.TextField()
    reply_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reply_datetime']
