from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from feedback.forms import FeedbackForm, DirectorFeedbackForm
from feedback.models import Feedback


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

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        form = DirectorFeedbackForm(request.POST, request.FILES)

        if form.is_valid():
            messages.success(request, f"Ваше обращение успешно отправлено директору")
            return redirect("feedback:director_feedback")
        else:
            self.context_object["form"] = form
            messages.error(request, f"Произошла ошибка, проверьте правильность данных")
            return render(request, self.template_name, self.context_object)
