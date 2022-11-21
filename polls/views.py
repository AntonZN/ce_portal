
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView
from view_breadcrumbs import ListBreadcrumbMixin

from .models import Choices, Questions, Answer, Form, Responses
import json
import random
import string

User = get_user_model()


class PollList(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    template_name = "index/list.html"
    model = Form
    paginate_by = 30
    context_object_name = "poll_list"
    queryset = Form.objects.all()


@staff_member_required
def index(request):
    forms = Form.objects.filter(creator=request.user)
    return render(request, "index/index.html", {"forms": forms})


@staff_member_required
def create_form(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data["title"]
        code = "".join(
            random.choice(string.ascii_letters + string.digits) for x in range(30)
        )
        choices = Choices(choice="Вариант ответа")
        choices.save()
        question = Questions(
            question_type=Questions.NO_MULTIPLE,
            question="Новый вопрос",
            required=False,
        )
        question.save()
        question.choices.add(choices)
        question.save()
        form = Form(code=code, title=title, creator=request.user)
        form.save()
        form.questions.add(question)
        form.save()
        return JsonResponse({"message": "Sucess", "code": code})


@staff_member_required
def edit_form(request, code):
    form_info = get_object_or_404(Form, code=code)

    return render(request, "index/form.html", {"code": code, "form": form_info})


@staff_member_required
def edit_title(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        data = json.loads(request.body)
        if len(data["title"]) > 0:
            form_info.title = data["title"]
            form_info.save()
        else:
            form_info.title = form_info.title[0]
            form_info.save()
        return JsonResponse({"message": "Success", "title": form_info.title})


@staff_member_required
def edit_description(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        data = json.loads(request.body)
        form_info.description = data["description"]
        form_info.save()
        return JsonResponse(
            {"message": "Success", "description": form_info.description}
        )


@staff_member_required
def edit_bg_color(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        data = json.loads(request.body)
        form_info.background_color = data["bgColor"]
        form_info.save()
        return JsonResponse(
            {"message": "Success", "bgColor": form_info.background_color}
        )


@staff_member_required
def edit_text_color(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        data = json.loads(request.body)
        form_info.text_color = data["textColor"]
        form_info.save()
        return JsonResponse({"message": "Success", "textColor": form_info.text_color})


@staff_member_required
def edit_setting(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        data = json.loads(request.body)
        form_info.collect_email = data["collect_email"]
        form_info.is_quiz = data["is_quiz"]
        form_info.authenticated_responder = data["authenticated_responder"]
        form_info.confirmation_message = data["confirmation_message"]
        form_info.edit_after_submit = data["edit_after_submit"]
        form_info.allow_view_score = data["allow_view_score"]
        form_info.save()
        return JsonResponse({"message": "Success"})


@staff_member_required
def delete_form(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "DELETE":
        # Delete all questions and choices
        for i in form_info.questions.all():
            for j in i.choices.all():
                j.delete()
            i.delete()
        for i in Responses.objects.filter(response_to=form_info):
            for j in i.response.all():
                j.delete()
            i.delete()
        form_info.delete()
        return JsonResponse({"message": "Success"})


@staff_member_required
def edit_question(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        data = json.loads(request.body)
        question_id = data["id"]
        question = Questions.objects.filter(id=question_id)
        if question.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else:
            question = question[0]
        question.question = data["question"]
        question.question_type = data["question_type"]
        question.required = data["required"]
        if data.get("score"):
            question.score = data["score"]
        if data.get("answer_key"):
            question.answer_key = data["answer_key"]
        question.save()
        return JsonResponse({"message": "Success"})


@staff_member_required
def edit_choice(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        data = json.loads(request.body)
        choice_id = data["id"]
        choice = Choices.objects.filter(id=choice_id)
        if choice.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else:
            choice = choice[0]
        choice.choice = data["choice"]
        if data.get("is_answer"):
            choice.is_answer = data["is_answer"]
        choice.save()
        return JsonResponse({"message": "Success"})


@staff_member_required
def add_choice(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        data = json.loads(request.body)
        choice = Choices(choice="Вариант ответа")
        choice.save()
        form_info.questions.get(pk=data["question"]).choices.add(choice)
        form_info.save()
        return JsonResponse(
            {"message": "Success", "choice": choice.choice, "id": choice.id}
        )


@staff_member_required
def remove_choice(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        data = json.loads(request.body)
        choice = Choices.objects.filter(pk=data["id"])
        if choice.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else:
            choice = choice[0]
        choice.delete()
        return JsonResponse({"message": "Success"})


@staff_member_required
def get_choice(request, code, question):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "GET":
        question = Questions.objects.filter(id=question)
        if question.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else:
            question = question[0]
        choices = question.choices.all()
        choices = [
            {"choice": i.choice, "is_answer": i.is_answer, "id": i.id} for i in choices
        ]
        return JsonResponse(
            {
                "choices": choices,
                "question": question.question,
                "question_type": question.question_type,
                "question_id": question.id,
            }
        )


@staff_member_required
def add_question(request, code):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "POST":
        choices = Choices(choice="Вариант 1")
        choices.save()
        question = Questions(
            question_type="multiple choice",
            question="Новый вопрос",
            required=False,
        )
        question.save()
        question.choices.add(choices)
        question.save()
        form_info.questions.add(question)
        form_info.save()
        return JsonResponse(
            {
                "question": {
                    "question": "Новый вопрос",
                    "question_type": "multiple choice",
                    "required": False,
                    "id": question.id,
                },
                "choices": {
                    "choice": "Вариант 1",
                    "is_answer": False,
                    "id": choices.id,
                },
            }
        )


@staff_member_required
def delete_question(request, code, question):
    form_info = get_object_or_404(Form, code=code)

    if request.method == "DELETE":
        question = Questions.objects.filter(id=question)
        if question.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else:
            question = question[0]
        for i in question.choices.all():
            i.delete()
            question.delete()
        return JsonResponse({"message": "Success"})


@staff_member_required
def score(request, code):
    form_info = get_object_or_404(Form, code=code)

    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        return render(request, "index/score.html", {"form": form_info})


@staff_member_required
def edit_score(request, code):
    form_info = get_object_or_404(Form, code=code)

    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question_id = data["question_id"]
            question = form_info.questions.filter(id=question_id)
            if question.count() == 0:
                return HttpResponseRedirect(reverse("edit_form", args=[code]))
            else:
                question = question[0]
            score = data["score"]
            if score == "":
                score = 0
            question.score = score
            question.save()
            return JsonResponse({"message": "Success"})


@staff_member_required
def answer_key(request, code):
    form_info = get_object_or_404(Form, code=code)

    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question = Questions.objects.filter(id=data["question_id"])
            if question.count() == 0:
                return HttpResponseRedirect(reverse("edit_form", args=[code]))
            else:
                question = question[0]
            if (
                question.question_type == "short"
                or question.question_type == "paragraph"
            ):
                question.answer_key = data["answer_key"]
                question.save()
            else:
                for i in question.choices.all():
                    i.is_answer = False
                    i.save()
                if question.question_type == "multiple choice":
                    choice = question.choices.get(pk=data["answer_key"])
                    choice.is_answer = True
                    choice.save()
                else:
                    for i in data["answer_key"]:
                        choice = question.choices.get(id=i)
                        choice.is_answer = True
                        choice.save()
                question.save()
            return JsonResponse({"message": "Success"})


@staff_member_required
def feedback(request, code):
    form_info = get_object_or_404(Form, code=code)

    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question = form_info.questions.get(id=data["question_id"])
            question.feedback = data["feedback"]
            question.save()
            return JsonResponse({"message": "Success"})


@login_required
def view_form(request, code):
    form_info = get_object_or_404(Form, code=code)

    if form_info.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
    return render(request, "index/view_form.html", {"form": form_info})


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@login_required
def submit_form(request, code):
    form_info = get_object_or_404(Form, code=code)
    initial_code = code
    if Responses.objects.filter(responder=request.user, response_to=form_info).exists():
        messages.success(request, "Ошибка. Вы уже проходили эту форму")
        return HttpResponseRedirect(
            reverse(
                "view_form",
                kwargs={"code": initial_code},
            )
        )

    if request.method == "POST":
        code = "".join(
            random.choice(string.ascii_letters + string.digits) for x in range(20)
        )
        if form_info.authenticated_responder:
            response = Responses(
                response_code=code,
                response_to=form_info,
                responder_ip=get_client_ip(request),
                responder=request.user,
            )
            response.save()
        else:
            if not form_info.collect_email:
                response = Responses(
                    response_code=code,
                    response_to=form_info,
                    responder_ip=get_client_ip(request),
                )
                response.save()
            else:
                response = Responses(
                    response_code=code,
                    response_to=form_info,
                    responder_ip=get_client_ip(request),
                    responder_email=request.POST["email-address"],
                )
                response.save()

        for i in request.POST:
            if i == "csrfmiddlewaretoken" or i == "email-address":
                continue
            question = form_info.questions.get(id=i)

            for j in request.POST.getlist(i):
                answer = Answer(answer=j, answer_to=question)
                answer.save()
                response.response.add(answer)
                response.save()

        messages.success(request, form_info.confirmation_message)

        return HttpResponseRedirect(
            reverse(
                "polls:view_form",
                kwargs={"code": initial_code},
            )
        )


@login_required
def responses(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    form_info = get_object_or_404(Form, code=code)

    responsesSummary = []
    choiceAnswered = {}
    filteredResponsesSummary = {}
    for question in form_info.questions.all():
        answers = Answer.objects.filter(answer_to=question.id)
        if (
            question.question_type == "multiple choice"
            or question.question_type == "checkbox"
        ):
            choiceAnswered[question.question] = choiceAnswered.get(
                question.question, {}
            )
            for answer in answers:
                choice = answer.answer_to.choices.get(id=answer.answer).choice
                choiceAnswered[question.question][choice] = (
                    choiceAnswered.get(question.question, {}).get(choice, 0) + 1
                )
        responsesSummary.append({"question": question, "answers": answers})
    for answr in choiceAnswered:
        filteredResponsesSummary[answr] = {}
        keys = choiceAnswered[answr].values()
        for choice in choiceAnswered[answr]:
            filteredResponsesSummary[answr][choice] = choiceAnswered[answr][choice]

    return render(
        request,
        "index/responses.html",
        {
            "form": form_info,
            "responses": Responses.objects.filter(response_to=form_info),
            "responsesSummary": responsesSummary,
            "filteredResponsesSummary": filteredResponsesSummary,
        },
    )


@login_required
def response(request, code, response_code):
    form_info = get_object_or_404(Form, code=code)

    if not form_info.allow_view_score:
        if form_info.creator != request.user:
            return HttpResponseRedirect(reverse("403"))
    total_score = 0
    score = 0
    responseInfo = Responses.objects.filter(response_code=response_code)
    if responseInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        responseInfo = responseInfo[0]
    if form_info.is_quiz:
        for i in form_info.questions.all():
            total_score += i.score
        for i in responseInfo.response.all():
            if (
                i.answer_to.question_type == "short"
                or i.answer_to.question_type == "paragraph"
            ):
                if i.answer == i.answer_to.answer_key:
                    score += i.answer_to.score
            elif i.answer_to.question_type == "multiple choice":
                answerKey = None
                for j in i.answer_to.choices.all():
                    if j.is_answer:
                        answerKey = j.id
                if answerKey is not None and int(answerKey) == int(i.answer):
                    score += i.answer_to.score
        _temp = []
        for i in responseInfo.response.all():
            if i.answer_to.question_type == "checkbox" and i.answer_to.pk not in _temp:
                answers = []
                answer_keys = []
                for j in responseInfo.response.filter(answer_to__pk=i.answer_to.pk):
                    answers.append(int(j.answer))
                    for k in j.answer_to.choices.all():
                        if k.is_answer and k.pk not in answer_keys:
                            answer_keys.append(k.pk)
                    _temp.append(i.answer_to.pk)
                if answers == answer_keys:
                    score += i.answer_to.score
    return render(
        request,
        "index/response.html",
        {
            "form": form_info,
            "response": responseInfo,
            "score": score,
            "total_score": total_score,
        },
    )


@staff_member_required
def edit_response(request, code, response_code):
    form_info = get_object_or_404(Form, code=code)

    response = Responses.objects.filter(
        response_code=response_code, response_to=form_info
    )
    if response.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        response = response[0]
    if form_info.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        if response.responder != request.user:
            return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        if form_info.authenticated_responder and not response.responder:
            response.responder = request.user
            response.save()
        if form_info.collect_email:
            response.responder_email = request.POST["email-address"]
            response.save()
        # Deleting all existing answers
        for i in response.response.all():
            i.delete()
        for i in request.POST:
            # Excluding csrf token and email address
            if i == "csrfmiddlewaretoken" or i == "email-address":
                continue
            question = form_info.questions.get(id=i)
            for j in request.POST.getlist(i):
                answer = Answer(answer=j, answer_to=question)
                answer.save()
                response.response.add(answer)
                response.save()
        if form_info.is_quiz:
            return HttpResponseRedirect(
                reverse("response", args=[form_info.code, response.response_code])
            )
        else:
            return render(
                request,
                "index/form_response.html",
                {"form": form_info, "code": response.response_code},
            )
    return render(
        request, "index/edit_response.html", {"form": form_info, "response": response}
    )


def delete_responses(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    form_info = get_object_or_404(Form, code=code)

    if request.method == "DELETE":
        responses = Responses.objects.filter(response_to=form_info)
        for response in responses:
            for i in response.response.all():
                i.delete()
            response.delete()
        return JsonResponse({"message": "Success"})
