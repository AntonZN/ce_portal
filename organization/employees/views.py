from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.views.generic import ListView, DetailView
from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin

from organization.employees.models import Employee
from organization.models import Department


class EmployeeList(LoginRequiredMixin, ListBreadcrumbMixin, ListView):
    template_name = "employees/employee_list.html"
    model = Employee
    context_object_name = "employees"
    paginate_by = 25

    def get_queryset(self):
        params = self.request.GET
        queryset = Employee.objects.all()

        query = params.get("query", None)

        if query:
            query = query.strip()
            queryset = queryset.filter(
                Q(fio__icontains=query)
                | Q(username__icontains=query)
                | Q(position__name__icontains=query)
                | Q(department__name__icontains=query)
            )

        if params.get("department_id", None):
            department_id = params.get("department_id")
            department = Department.objects.get(id=department_id)
            queryset = department.supervisor.get_descendants(include_self=True)

        if params.get("position_id", None):
            queryset = queryset.filter(position_id=params.get("position_id"))

        page = params.get("page")
        paginator = Paginator(queryset, self.paginate_by)
        queryset = paginator.get_page(page)

        return queryset

    def get(self, request, *args, **kwargs):
        context = dict()
        queryset = self.get_queryset()
        is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
        context.update({"employees": queryset})

        if is_ajax_request:
            html = render_to_string(
                template_name="employees/employees_results_partial.html",
                context=context,
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)

        if request.htmx:
            return render(request, "employees/employees_results_partial.html", context=context)

        return render(request, "employees/employee_list.html", context=context)


class EmployeeDetail(LoginRequiredMixin, DetailBreadcrumbMixin, DetailView):
    template_name = "employees/employee_detail.html"
    model = Employee
    context_object_name = "employee"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["children_employees"] = self.object.get_children()
        return context
