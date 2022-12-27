from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from post_office import mail

from feedback.forms import FeedbackForm, DirectorFeedbackForm, IdeaFeedbackForm
from feedback.models import Feedback, FeedbackForDirector, IdeaFeedback
from organization.models import OrganizationConfig


class FeedbackView(LoginRequiredMixin, View):

    template_name = "feedbacks/question.html"
    context_object = {}

    def get(self, request):
        if request.GET.get("review"):
            feedback = Feedback(type=Feedback.REVIEW)
        elif request.GET.get("idea"):
            feedback = Feedback(type=Feedback.IDEA)
        else:
            feedback = Feedback(type=Feedback.QUESTION)

        form = FeedbackForm(instance=feedback)

        if Feedback.objects.filter(
                author=request.user, created__gt=timezone.now() - timedelta(days=1)
        ).exists():
            self.context_object["exist"] = True
        else:
            self.context_object["exist"] = False

        self.context_object["form"] = form

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        if Feedback.objects.filter(
            author=request.user, created__gt=timezone.now() - timedelta(days=1)
        ).exists():
            messages.success(
                request,
                f"Ваше обращение уже зафиксировано, повторите попытку через день",
            )
            return redirect("feedback:org_feedback")

        feedback = Feedback(author=request.user)

        form = FeedbackForm(request.POST, request.FILES, instance=feedback)

        if form.is_valid():
            form.save()
            messages.success(request, f"Ваше обращение успешно создано")
            return redirect("feedback:org_feedback")
        else:
            self.context_object["form"] = form
            messages.error(request, f"Произошла ошибка, проверьте правильность данных")
            return render(request, self.template_name, self.context_object)


class DirectorFeedbackView(LoginRequiredMixin, View):

    template_name = "feedbacks/question_to_director.html"
    context_object = {}

    def get(self, request):

        form = DirectorFeedbackForm()
        self.context_object["form"] = form

        if FeedbackForDirector.objects.filter(
                author=request.user, created__gt=timezone.now() - timedelta(days=1)
        ).exists():
            self.context_object["exist"] = True
        else:
            self.context_object["exist"] = False

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        if FeedbackForDirector.objects.filter(
            author=request.user, created__gt=timezone.now() - timedelta(days=1)
        ).exists():
            messages.success(
                request,
                f"Ваше обращение уже зафиксировано, повторите попытку через день",
            )
            return redirect("feedback:director_feedback")

        feedback = FeedbackForDirector(author=request.user)

        form = DirectorFeedbackForm(request.POST, request.FILES, instance=feedback)

        if form.is_valid():
            form.save()
            messages.success(request, f"Ваше обращение успешно отправлено директору")
            return redirect("feedback:director_feedback")
        else:
            self.context_object["form"] = form
            messages.error(request, f"Произошла ошибка, проверьте правильность данных")
            return render(request, self.template_name, self.context_object)


class IdeaFeedbackView(LoginRequiredMixin, View):

    template_name = "ideas.html"
    context_object = {}

    def post(self, request, *args, **kwargs):

        if IdeaFeedback.objects.filter(
                author=request.user, created__gt=timezone.now() - timedelta(days=1)
        ).exists():
            messages.success(
                request,
                f"Ваша идея уже зафиксирована, повторите попытку через день",
            )
            return redirect("ideas")

        feedback = IdeaFeedback(author=request.user)

        form = IdeaFeedbackForm(request.POST, request.FILES, instance=feedback)

        if form.is_valid():
            form.save()
            config = OrganizationConfig.objects.get()
            if config.ideas_email:
                mail.send(
                    config.ideas_email,
                    settings.DEFAULT_FROM_EMAIL,
                    template="new_idea",
                    context={
                        "employee": request.user,
                        "topic": form.cleaned_data["topic"],
                        "text": form.cleaned_data["text"]
                    },
                )
            messages.success(request, f"Ваше идея успешно зафиксирована")
            return redirect("ideas")
        else:
            self.context_object["form"] = form
            messages.error(request, f"Произошла ошибка, проверьте правильность данных")
            return render(request, self.template_name, self.context_object)


class MyFeedbackView(LoginRequiredMixin, View):
    template_name = "feedbacks/my.html"
    context_object = {}

    def get(self, request):
        feedbacks = Feedback.objects.filter(author=request.user)
        ideas = IdeaFeedback.objects.filter(author=request.user)
        self.context_object["feedbacks"] = feedbacks
        self.context_object["ideas"] = ideas
        return render(request, self.template_name, self.context_object)
