from django.contrib import admin

# Register your models here.

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import EditorSignUpForm, ChiefSignUpForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = EditorSignUpForm
    form = ChiefSignUpForm
    model = User
    # list_display = ['email', 'username', 'name']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
