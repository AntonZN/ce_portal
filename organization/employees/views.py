from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.views import View
from django.views.generic import ListView

from organization.employees.models import Employee


class EmployeeListView(LoginRequiredMixin, View):
    template_name = "employees/employee_list.html"
    context_object = {}

    def get(self, request):
        return render(request, self.template_name, self.context_object)


class EmployeeList(ListView):
    template_name = "employees/employee_list.html"
    model = Employee
    context_object_name = "employees"

    def get_queryset(self):
        params = self.request.GET
        queryset = Employee.objects.filter(active=True)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        params = self.request.GET
        context = super().get_context_data(**kwargs)
        return context


class EmployeeDetail(LoginRequiredMixin, View):

    template_name = "employees/employee_detail.html"
    context_object = {}

    def get(self, request):
        return render(request, self.template_name, self.context_object)
