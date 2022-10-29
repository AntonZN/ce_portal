from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from organization.employees.froms import EmployeeForm, EmployeeContactsFormSet


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"


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
        employee_form = EmployeeForm(request.POST, request.FILES, instance=self.request.user)
        print(request.FILES)
        if employee_form.is_valid():
            employee_form.save()
            messages.success(
                request, f"Ваш профиль успешно обновлен"
            )
            return redirect("profile")

        else:
            employee_form = EmployeeForm(request.POST, instance=self.request.user)

            self.context_object["employee_form"] = employee_form

            messages.error(request, f"Invalid data. Please provide valid data.")
            return render(request, self.template_name, self.context_object)


def manage_employee_contacts(request):
    context_object = dict()
    employee_form = EmployeeForm(instance=request.user)
    employee_contacts_form = EmployeeContactsFormSet(instance=request.user)

    if request.method == 'POST':
        formset = EmployeeContactsFormSet(request.POST, instance=request.user)

        if formset.is_valid():
            formset.save()
            for obj in formset.deleted_objects:
                try:
                    obj.delete()
                except ValueError:
                    pass
            messages.success(
                request, f"Ваши контакты успешно обновлены"
            )
            return redirect("profile")
        else:
            messages.error(
                request, f"Проверьте правильность введенных данных"
            )

            context_object["employee_form"] = employee_form
            context_object["employee_contacts_form"] = formset
            return render(request, "profile.html", context_object)
