from django.contrib.auth import login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, FormView, DetailView, ListView,
    UpdateView, TemplateView, DeleteView)
from django.views.generic.edit import FormMixin

from django.urls import reverse_lazy

from .decorators import editor_required, chief_required
from .forms import *
from .models import *


class HomeView(ListView):
    template_name = 'blog/view_post.html'
    model = Post
    paginate_by = 10
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
        return redirect('post_list')


@method_decorator([login_required], name='dispatch')
class PostListView(ListView):
    ordering = ('published_date',)
    context_object_name = 'post_list'
    template_name = 'blog/post_list.html'
    paginate_by = 10

    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        return Post.objects.all()   #filter(owner_id=user.id, is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['users'] = False
        check = User.objects.filter(username=self.request.user, is_chief=True)
        if check:
            context['users'] = True
        return context


# @method_decorator([login_required], name='dispatch')
class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(blog_id=self.get_object().id)

        # provide the columns name in values_list
        context['comments'] = comments.values_list('user_id__username', 'comment', 'id')
        context['form'] = CommentForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        comment = form.save(commit=False)
        comment.blog = self.get_object()
        comment.user = self.request.user
        form.save()
        return super(PostDetailView, self).form_valid(form)


@method_decorator([login_required], name='dispatch')
class PostUpdateView(UpdateView):
    template_name = 'blog/add_post_form.html'
    model = Post
    fields = ['title', 'text']
    success_url = '/post_list'


@method_decorator([login_required, chief_required], name='dispatch')
class PostApprovalListView(ListView):
    template_name = 'blog/post_approve_list.html'
    ordering = ('published_date',)
    context_object_name = 'postApprove'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_approve=False)


@method_decorator([login_required, editor_required], name='dispatch')
class PostApprovalView(UpdateView):
    template_name = 'blog/post_approval.html'
    model = Post
    fields = ['is_approve']
    success_url = '/post_list'


@method_decorator([login_required], name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


@method_decorator([login_required], name='dispatch')
class CommentReplyView(FormMixin, DetailView):
    model = Comment
    form_class = ReplyForm
    template_name = 'blog/comment_reply.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('comment_reply', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        # print(self.pk)
        context = super(CommentReplyView, self).get_context_data(**kwargs)
        reply = Reply.objects.filter(which_comment_id=self.get_object().id)

        # provide the columns name in values_list
        context['reply'] = reply.values_list('user_id__username', 'reply')
        context['form'] = ReplyForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        reply = form.save(commit=False)
        reply.which_comment = self.get_object()
        # current_user = auth.get_user(self.request)
        reply.user = self.request.user
        form.save()
        return super(CommentReplyView, self).form_valid(form)
