from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from organization.employees.froms import EmployeeUpdateForm
from organization.employees.models import Employee


class HomeView(TemplateView):
    template_name = "home.html"


class ProfileView(LoginRequiredMixin, View):

    template_name = "profile.html"
    context_object = {}

    def get(self, request):
        employee_form = EmployeeUpdateForm(instance=self.request.user)

        self.context_object["employee_form"] = employee_form

        return render(request, self.template_name, self.context_object)


class ProfileUpdateView(LoginRequiredMixin, View):

    template_name = "profile_update.html"
    context_object = {}

    def post(self, request, *args, **kwargs):
        employee_form = EmployeeUpdateForm(data=request.POST, instance=self.request.user)

        if employee_form.is_valid():
            employee_form.save()

            messages.success(
                request, f"Your account has successfully " f"been updated!"
            )
            return redirect("blog:author_profile_details")

        else:
            employee_form = EmployeeUpdateForm(data=request.POST, instance=self.request.user)

            self.context_object["employee_form"] = employee_form

            messages.error(request, f"Invalid data. Please provide valid data.")
            return render(request, self.template_name, self.context_object)
