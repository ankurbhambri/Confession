from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class EditorSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
        strip=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
        strip=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Password'}),

        }

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_editor = True
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ChiefSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(), strip=True)
    last_name = forms.CharField(widget=forms.TextInput(), strip=True)
    email = forms.EmailField(widget=forms.EmailInput())

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_chief = True
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label="", help_text="",
                              strip=True, widget=forms.Textarea())

    class Meta:
        model = Comment
        fields = ('comment',)


class ReplyForm(forms.ModelForm):
    reply = forms.CharField(label="", help_text="",
                            strip=True, widget=forms.Textarea())

    class Meta:
        model = Reply
        fields = ('reply',)


class UserInfoForm(forms.ModelForm):
    """Image upload form."""
    # image = forms.ImageField()

    class Meta:
        model = UserInfo
        fields = ('avatar', 'intro', 'bio',)
