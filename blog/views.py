from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from django.views.generic.edit import FormMixin, FormView
from django.urls import reverse_lazy

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .decorators import editor_required, chief_required
from .forms import *
from .models import *
from notifications.signals import send, recieve


@receiver(pre_save, sender=Post)
def function_pre_save(sender, **kwargs):
    print(sender, kwargs)
    print('function for pre save called')


@receiver(post_save, sender=Post)
def function_post_save(sender, instance, created, **kwargs):
    print('function for post save called')


class HomeView(ListView):
    template_name = 'blog/view_post.html'
    model = Post
    paginate_by = 10
    queryset = Post.objects.filter(is_approve=True)

    def get_queryset(self):
        # user = User.objects.get(username=self.request.user)
        return Post.objects.filter(
            is_approve=True,
            is_deleted=False
        )

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['notifications'] = recieve(self.request.user)
        return context


class CustomLoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = 'post_list'

    def form_valid(self, form):
        user = authenticate(
            username=form.data['username'],
            password=form.data['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return super().form_valid(form)
        else:
            messages.error(self.request, 'username or password not correct')
            return HttpResponseRedirect(self.get_success_url())


class EditorSignUpView(CreateView):
    model = User
    form_class = EditorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Editor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class ChiefSignUpView(CreateView):
    model = User
    form_class = ChiefSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Moderator'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('post_list')


@method_decorator([login_required], name='dispatch')
class IndexView(CreateView):
    """
    Create new blog
    """
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
        # user = User.objects.get(username=self.request.user)
        return Post.objects.filter(
            owner_id=self.request.user,
            is_deleted=False
        )

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['users'] = False
        check = User.objects.filter(
            username=self.request.user,
            is_chief=True
        )
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
        context['comments'] = comments.values_list(
            'user_id__username', 'comment', 'id')
        context['reply'] = Reply.objects.filter(blog_id=self.object.pk)
        context['form'] = CommentForm(initial={'post': self.object})
        return context

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
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
    '''
        View to list of all post that need to be approved.
    '''
    template_name = 'blog/post_approve_list.html'
    ordering = ('published_date',)
    context_object_name = 'postApprove'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_approve=False)


@method_decorator([login_required, chief_required], name='dispatch')
class PostApprovalView(UpdateView):
    '''
        View create a form to approve the blog by moderator.
    '''
    template_name = 'blog/post_approval.html'
    model = Post
    fields = ['is_approve']
    # success_url = reverse_lazy('post_approve_list')

    def get_success_url(self):
        try:
            post = Post.objects.get(id=self.object.pk)
            if post.is_approve:
                verb = "%s Approved" % post.title
            else:
                verb = "%s Not Approved" % post.title
        except ObjectDoesNotExist:
            pass
        send(
            sender=self.request.user,
            recipient=User.objects.get(id=self.object.owner_id),
            verb=verb
        )
        return reverse_lazy('post_approve_list')


@method_decorator([login_required, chief_required], name='dispatch')
class PostApprovedView(ListView):
    '''
        View to show the approved post by loged in moderator
    '''
    template_name = 'blog/post_approve_list.html'
    ordering = ('published_date',)
    context_object_name = 'postApprove'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_approve=True)


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

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.which_comment = self.get_object()
        b = Comment.objects.filter(
            id=self.object.pk).values_list('blog_id__id')
        p = Post.objects.filter(id=b.values('blog_id')[0]['blog_id'])
        reply.blog = p[0]
        reply.user = self.request.user
        form.save()
        return super(CommentReplyView, self).form_valid(form)
