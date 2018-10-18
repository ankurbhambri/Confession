from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import *


class EditorSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_editor = True
        user.save()
        Editor.objects.create(user=user)
        return user


class ChiefSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_chief = True
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label="", help_text="", widget=forms.Textarea())

    class Meta:
        model = Comment
        fields = ('comment',)


class ReplyForm(forms.ModelForm):
    reply = forms.CharField(label="", help_text="", widget=forms.Textarea())

    class Meta:
        model = Reply
        fields = ('reply',)
