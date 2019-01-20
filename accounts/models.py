import datetime
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save

from blog.models import *


REQUEST_CHOICES = (
    ('api', 'api'),
    ('template', 'template')
)
DEGREE = (
    ('metric', 'Metriculate'),
    ('inter', 'Intermediate'),
    ('grad', 'Graduation'),
    ('pg', 'Post Graduation'),
    ('dr', 'Doctorate'),
)
YEAR_CHOICES = [(r, r) for r in range(1950, datetime.date.today().year + 5)]
month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
MONTH = [(i.lower(), i) for i in month_list]
RATING_CHOICES = [(r, r) for r in range(0, 101)]


class UserInfo(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    avatar = models.ImageField(upload_to='profiles', blank=True, default='/profiles/python.png')
    intro = models.CharField(max_length=1000, blank=True, null=True)
    bio = RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField()


# Signal to create a user profile whenever a new user create.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance, slug=instance.username)


post_save.connect(create_user_profile, sender=User)


class SkillSet(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    skill = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        blank=False,
        null=False,
        default=0
    )


class Qualification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    qualification = models.CharField(
        max_length=255,
        choices=DEGREE,
        null=False
    )
    specialization = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=10, null=False)
    from_year = models.IntegerField(('year'), choices=YEAR_CHOICES)
    completion_year = models.IntegerField(('year'), choices=YEAR_CHOICES)
    achievement = models.TextField(blank=True)  # RichTextUploadingField()


class Experience(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    designation = models.CharField(max_length=255, null=False)
    org_name = models.CharField(max_length=255, null=True)
    start_month = models.CharField(max_length=255, choices=MONTH)
    start_year = models.IntegerField(('year'), choices=YEAR_CHOICES)
    end_month = models.CharField(max_length=255, choices=MONTH, blank=True, null=True)
    completion_year = models.IntegerField(('year'), choices=YEAR_CHOICES, blank=True, null=True)
    present_working = models.BooleanField(default=False)
    description = models.CharField(max_length=1000)
