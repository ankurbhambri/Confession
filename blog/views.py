from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, FormView, DetailView, ListView,
                                  UpdateView, TemplateView)

from .decorators import editor_required, chief_required
from .forms import *
from .models import *


class HomeView(ListView):
    template_name = 'blog/view_post.html'
    model = Post
    paginate_by = 2
    queryset = Post.objects.filter(is_approve=True)


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class EditorSignUpView(CreateView):
    model = User
    form_class = EditorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'editor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('post')


class ChiefSignUpView(CreateView):
    model = User
    form_class = ChiefSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Chief'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('post_list')


@method_decorator([login_required], name='dispatch')
class IndexView(CreateView):
    model = Post
    fields = ('title', 'text', )
    template_name = 'blog/add_post_form.html'
    success_url = 'post_list'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.owner = self.request.user
        post.published_date = timezone.now()
        post.save()
        messages.success(self.request, 'The post was created with success! Go ahead and add some tags now.')
        return redirect('post_list')


@method_decorator([login_required], name='dispatch')
class PostListView(ListView):
    ordering = ('published_date',)
    context_object_name = 'post_list'
    template_name = 'blog/post_list.html'
    paginate_by = 2
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['users'] = False
        check = User.objects.filter(username=self.request.user, is_chief=True)
        if check:
            context['users'] = True
        context['post'] = self.queryset
        return context


# @method_decorator([login_required], name='dispatch')
class PostDetailView(DetailView):
    model = Post


@method_decorator([login_required], name='dispatch')
class PostUpdateView(UpdateView):
    template_name = 'blog/add_post_form.html'
    model = Post
    fields = ['title', 'text']
    success_url = '/post_list'


@method_decorator([login_required, chief_required], name='dispatch')
class PostApprovalListView(FormView):
    template_name = 'blog/post_list.html'
    ordering = ('published_date',)
    # context_object_name = 'post_approval_list'


@method_decorator([login_required, editor_required], name='dispatch')
class PostApprovalView(UpdateView):
    template_name = 'blog/post_approval.html'
    model = Post
    fields = ['is_approve']
    success_url = '/post_list'
