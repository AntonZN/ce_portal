from datetime import datetime
from functools import cached_property

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin

from blog.models import News
from feedback.forms import IdeaFeedbackForm
from organization.employees.froms import EmployeeForm, EmployeeContactsFormSet
from organization.employees.models import Employee
from organization.models import OrganizationConfig, Banner
from filer.models import Folder, File


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = OrganizationConfig.objects.get()
        context["phrases"] = config.phrases.all()
        context["birthdays_today"] = Employee.manager.get_birthdays()
        context["birthdays_cur_month"] = Employee.objects.filter(birthday__month=datetime.now().month).order_by("birthday__day")
        # context["birthdays_upcoming"] = Employee.manager.get_upcoming_birthdays(include_day=False, days=14)
        context["main_news"] = News.main.all()
        context["latest_news"] = News.public.exclude(home_view=True)[:6]
        context["new_employees"] = Employee.new.all()[:9]
        context["banners"] = Banner.objects.filter(is_view=True).order_by("order")
        context["folders"] = Folder.objects.all()

        return context


class ProfileView(LoginRequiredMixin, View):

    template_name = "profile.html"
    context_object = {}

    def get(self, request):
        employee_form = EmployeeForm(instance=self.request.user)
        employee_contacts_form = EmployeeContactsFormSet(instance=self.request.user)
        self.context_object["employee_form"] = employee_form
        self.context_object["employee_contacts_form"] = employee_contacts_form

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        employee_form = EmployeeForm(
            request.POST, request.FILES, instance=self.request.user
        )
        if employee_form.is_valid():
            employee_form.save()
            messages.success(request, f"Ваш профиль успешно обновлен")
            return redirect("profile")

        else:
            employee_form = EmployeeForm(request.POST, instance=self.request.user)

            self.context_object["employee_form"] = employee_form

            messages.error(request, f"Invalid data. Please provide valid data.")
            return render(request, self.template_name, self.context_object)


def manage_employee_contacts(request):
    context_object = dict()
    employee_form = EmployeeForm(instance=request.user)

    if request.method == "POST":
        formset = EmployeeContactsFormSet(request.POST, instance=request.user)

        if formset.is_valid():
            formset.save()
            for obj in formset.deleted_objects:
                try:
                    obj.delete()
                except ValueError:
                    pass
            messages.success(request, f"Ваши контакты успешно обновлены")
            return redirect("profile")
        else:
            messages.error(request, f"Проверьте правильность введенных данных")

            context_object["employee_form"] = employee_form
            context_object["employee_contacts_form"] = formset
            return render(request, "profile.html", context_object)


class AlbumList(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    template_name = "albums/list.html"
    model = News
    paginate_by = 15
    context_object_name = "folders"
    ordering = ["-date_published"]

    @cached_property
    def crumbs(self):
        return [
            (
                "Фотоальбомы",
                reverse("album_list", kwargs={}),
            ),
        ]
    def get_queryset(self):
        config = OrganizationConfig.objects.get()
        return Folder.objects.filter(parent=config.albums_folder)


class AlbumDetail(LoginRequiredMixin, DetailBreadcrumbMixin, DetailView):
    model = Folder
    template_name = "albums/detail.html"
    context_object_name = "folder"
    breadcrumb_use_pk = True

    @cached_property
    def crumbs(self):
        return [
            (
                "Фотоальбомы",
                reverse("album_list", kwargs={}),
            ),
            (self.object.name, ""),
        ]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        files = File.objects.filter(folder=self.object)
        context["photos"] = files
        return context


class AboutDetail(LoginRequiredMixin, DetailBreadcrumbMixin, TemplateView):
    template_name = "about.html"

    @cached_property
    def crumbs(self):
        return [
            (
                "О компании",
                reverse("about", kwargs={}),
            ),
        ]


class BankIdeas(LoginRequiredMixin, DetailBreadcrumbMixin, TemplateView):
    template_name = "bank_ideas.html"

    @cached_property
    def crumbs(self):
        return [
            (
                "Банк идей",
                reverse("ideas", kwargs={}),
            ),
        ]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = IdeaFeedbackForm()

        return context

