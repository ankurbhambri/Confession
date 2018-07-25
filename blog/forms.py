from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import *


class EditorSignUpForm(UserCreationForm):
    # interests = forms.ModelMultipleChoiceField(
    #     queryset=Post.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )

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
