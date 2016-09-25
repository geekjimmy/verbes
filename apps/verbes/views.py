from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView, FormView

from .forms import AttemptForm, UserMoodTenseForm, UserRegistrationForm
from .models import Attempt, Conjugation, UserMoodTense


class AttempView(TemplateView):
    template_name = 'attempt.html'

    def get_context_data(self):
        conjugation = Conjugation.objects.random(self.request.user)
        form = AttemptForm(initial={'conjugation': conjugation})

        success_rate = None
        if Attempt.objects.num_attempts(self.request):
            success_rate = 100 * (Attempt.objects.num_good_attempts(self.request) / Attempt.objects.num_attempts(self.request))
            success_rate = round(success_rate, 1)

        context = {
            'conjugation': conjugation,
            'form': form,
            'success_rate': success_rate
        }

        return context

class FeedbackView(View):
    def get(self, request):
        return redirect('attempt')

    def post(self, request):
        form = AttemptForm(request.POST)

        if not form.is_valid():
            return redirect('attempt')

        attempt = form.save(commit=False)

        # Save session so there is always one.
        request.session.save()

        if request.user.is_anonymous():
            attempt.user_session = Session.objects.filter(session_key=request.session.session_key).get()
        else:
            attempt.user = self.request.user

        attempt.save()

        success_rate = None
        if Attempt.objects.num_attempts(request):
            success_rate = 100 * (Attempt.objects.num_good_attempts(request) / Attempt.objects.num_attempts(request))
            success_rate = round(success_rate, 1)

        ctx = {
            'attempt': attempt,
            'conjugation': attempt.conjugation,
            'success_rate': success_rate
        }

        return render(
            request,
            'attempt_feedback.html',
            ctx
        )


class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('attempt')

    def form_valid(self, form):
        form.save(True)

        user = authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        login(self.request, user)

        return super().form_valid(form)


class ResultsView(TemplateView):
    template_name = 'results.html'

    def get_context_data(self):
        context = {}

        attempts = Attempt.objects.own(self.request).order_by('-created_time')
        paginator = Paginator(attempts, 10)
        page = self.request.GET.get('page')

        try:
            attempts = paginator.page(page)
        except PageNotAnInteger:
            attempts = paginator.page(1)
        except EmptyPage:
            attempts = paginator.page(paginator.num_pages)

        context['attempts'] = attempts

        success_rate = None
        if Attempt.objects.num_attempts(self.request):
            success_rate = 100 * (Attempt.objects.num_good_attempts(self.request) / Attempt.objects.num_attempts(self.request))
            success_rate = round(success_rate, 1)

        context['success_rate'] = success_rate

        return context


class UserMoodTenseView(FormView):
    template_name = 'mood_tense.html'
    form_class = UserMoodTenseForm
    success_url = reverse_lazy('user-mood-tense')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save(self.request.user)
        return super().form_valid(form)
