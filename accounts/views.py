
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView
)
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

from num2words import num2words

from .forms import *
from .models import *
from blog.models import User


@method_decorator([login_required], name='dispatch')
class UserInfoView(CreateView):
    model = UserInfo
    form_class = UserInfoForm
    template_name = 'accounts/userinfo_form.html'
    success_url = 'home'

    def form_valid(self, form):
        user_info = form.save(commit=False)
        user_info.user = self.request.user
        user_info.slug = self.request.user.username
        user_info.save()
        return redirect('home')


@method_decorator([login_required], name='dispatch')
class UserUpdateView(UpdateView):
    model = UserInfo
    form_class = UserInfoForm
    template_name = 'accounts/userinfo_form.html'

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'slug': self.kwargs['slug']})


@method_decorator([login_required], name='dispatch')
class SkillView(CreateView):
    model = SkillSet
    form_class = SkillsForm
    template_name = 'accounts/skills_form.html'
    success_url = reverse_lazy('qualification')

    def get_object(self, **kwargs):
        return UserInfo.objects.get(slug=self.kwargs['slug'])

    def form_valid(self, form, **kwargs):
        if 'save_and_return' in self.request.POST:
            comment = form.save(commit=False)
            comment.blog = self.get_object()
            comment.user = self.request.user
            form.save()
            return HttpResponseRedirect(reverse_lazy('skill', kwargs={'slug': self.kwargs['slug']}))
        elif 'submit' in self.request.POST:
            comment = form.save(commit=False)
            comment.blog = self.get_object()
            comment.user = self.request.user
            form.save()
            return HttpResponseRedirect(reverse_lazy('qualification', kwargs={'slug': self.kwargs['slug']}))


@method_decorator([login_required], name='dispatch')
class QualificationView(CreateView):
    model = Qualification
    form_class = QualificationForm
    template_name = 'accounts/qualification_form.html'
    success_url = reverse_lazy('experience')

    def get_object(self, **kwargs):
        return UserInfo.objects.get(slug=self.kwargs['slug'])

    def form_valid(self, form, **kwargs):
        if 'save_and_return' in self.request.POST:
            comment = form.save(commit=False)
            comment.blog = self.get_object()
            comment.user = self.request.user
            form.save()
            return HttpResponseRedirect(reverse_lazy('qualification', kwargs={'slug': self.kwargs['slug']}))
        elif 'submit' in self.request.POST:
            comment = form.save(commit=False)
            comment.blog = self.get_object()
            comment.user = self.request.user
            form.save()
            return HttpResponseRedirect(reverse_lazy('experience', kwargs={'slug': self.kwargs['slug']}))


@method_decorator([login_required], name='dispatch')
class ExperienceView(CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'accounts/experience_form.html'
    success_url = 'user_detail'

    def get_object(self, **kwargs):
        return UserInfo.objects.get(slug=self.kwargs['slug'])

    def form_valid(self, form, **kwargs):
        if 'save_and_return' in self.request.POST:
            comment = form.save(commit=False)
            comment.blog = self.get_object()
            comment.user = self.request.user
            form.save()
            return HttpResponseRedirect(reverse_lazy('experience', kwargs={'slug': self.kwargs['slug']}))
        elif 'submit' in self.request.POST:
            comment = form.save(commit=False)
            comment.blog = self.get_object()
            comment.user = self.request.user
            if form.cleaned_data['present_working']:
                if not form.cleaned_data['end_month']:
                    comment.end_month = None
                if not form.cleaned_data['completion_year']:
                    comment.completion_year = None
            comment.save()
            return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs={'slug': self.kwargs['slug']}))


# @method_decorator([login_required], name='dispatch')
class UserDetailView(DetailView, FormMixin):
    model = UserInfo
    form_class = ContactForm
    context_object_name = 'user_info'
    template_name = 'accounts/userdetail.html'

    def get_success_url(self):
        # return reverse_lazy('user_detail', kwargs={'slug': 'mashwani'})
        return reverse_lazy('greeting')

    def get_context_data(self, **kwargs):
        print(self.request.user.is_authenticated)
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['user_auth'] = self.request.user.is_authenticated
        context['user'] = User.objects.get(pk=self.object.pk)
        context['skill'] = SkillSet.objects.filter(user=self.object.pk)
        qualification = Qualification.objects.filter(user=self.object.pk)
        d = {}
        for i in range(len(qualification)):
            d[num2words(i+1).capitalize()] = qualification[i]
        context['qualification'] = d
        context['experience'] = Experience.objects.filter(user=self.object.pk)
        context['post'] = Post.objects.filter(
            owner_id=self.object.pk).order_by('-created_date')[:3]
        return context

    # @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        name = form.cleaned_data['name']
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['from_email'].strip()
        message = form.cleaned_data['message']
        msg = "Hi, I am %s and email: %s. \n\n\t%s" % (name, from_email, message)
        try:
            # send_mail(subject, msg, from_email, settings.EMAIL_HOST_USER)
            send_mail(subject, msg, settings.EMAIL_HOST_USER, ['confessionat9@gmail.com'])
            print("MAIL SEND SUCCESSFULLY")
        except Exception:
            print("MAIL NOT SEND")
        return super(UserDetailView, self).form_valid(form)


@method_decorator([login_required], name='dispatch')
class DeleteSkillView(DeleteView):
    model = SkillSet
    # success_url = reverse_lazy('user_detail')

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})


@method_decorator([login_required], name='dispatch')
class SkillUpdateView(UpdateView):
    model = SkillSet
    template_name = 'accounts/skills_form.html'
    # fields = ['skill', 'rating']
    form_class = SkillsForm

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})


# @method_decorator([login_required], name='dispatch')
# class SkillBatchUpdateView(UpdateView):
#     model = SkillSet
#     template_name = 'accounts/skills_form.html'
#     # fields = ['skill', 'rating']
#     form_class = SkillsForm

#     def get_success_url(self):
#         return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})


@method_decorator([login_required], name='dispatch')
class QualificationUpdateView(UpdateView):
    model = Qualification
    template_name = 'accounts/qualification_form.html'
    form_class = QualificationForm

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})


@method_decorator([login_required], name='dispatch')
class QualificationDeleteView(DeleteView):
    model = Qualification

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})


@method_decorator([login_required], name='dispatch')
class ExperienceUpdateView(UpdateView):
    model = Experience
    template_name = 'accounts/experience_form.html'
    form_class = ExperienceForm

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})


@method_decorator([login_required], name='dispatch')
class ExperienceDeleteView(DeleteView):
    model = Experience

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})

