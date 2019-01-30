from django import forms
from django.forms.models import inlineformset_factory
from django.forms import formset_factory

from .models import *


class UserInfoForm(forms.ModelForm):
    """Image upload form."""
    # image = forms.ImageField()

    class Meta:
        model = UserInfo
        fields = ('avatar', 'intro', 'bio',)


class SkillsForm(forms.ModelForm):

    class Meta:
        model = SkillSet
        fields = ('skill', 'rating',)
        widgets = {
            'skill': forms.TextInput(attrs={"placeholder": "eg. Java, Python etc"}),
            'rating': forms.TextInput(attrs={'type': 'range', 'step': '1'})
        }


# SkillsFormset = formset_factory(SkillsForm, extra=1)
# SkillsFormset = inlineformset_factory(SkillSet, fields=['skill', 'rating'], extra=1)


class QualificationForm(forms.ModelForm):

    class Meta:
        model = Qualification
        fields = ('qualification', 'specialization', 'grade', 'from_year', 'completion_year', 'achievement',)


class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        exclude = ('user',)


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
    )
    from_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'})
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Message', 'class': 'form-control'}),
    )
