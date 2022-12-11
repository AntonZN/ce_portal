from datetime import timedelta

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.middleware.csrf import get_token

from rest_framework.views import APIView
from sorl.thumbnail import get_thumbnail

from organization.employees.api.serializers import EmployeeSearchSerializer
from organization.employees.models import EmployeeLikes, Employee
from organization.models import Department, Filial, OrganizationConfig


class EmployeeSearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query", None)

        if query:
            query = query.strip()
            return Employee.objects.filter(
                Q(fio__icontains=query)
                | Q(username__icontains=query)
                | Q(position__name__icontains=query)
                | Q(department__name__icontains=query)
            )


class LikeEmployee(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Лайкнуть пользователя",
        responses={200: "OK"},
    )
    def post(self, request, employee_id, *args, **kwargs):
        context = {}
        employee = Employee.objects.get(id=employee_id)
        context["employee"] = employee
        context["csrf_token"] = get_token(request)

        if employee_id != request.user.id:
            critical_time = timezone.now() - timedelta(days=1)
            if EmployeeLikes.objects.filter(
                employee_id=employee_id, user=request.user, created__gt=critical_time
            ).exists():
                context["htmx_message"] = "Вы уже голосовали за этого сотрудника сегодня"
            else:
                EmployeeLikes.objects.create(
                    employee_id=employee_id, user=request.user
                )
                context["htmx_message"] = "Голос успешно засчитан"
        else:
            context["htmx_message"] = "Нельзя голосовать за себя"

        html = render_to_string(
            template_name="employees/employee_likes.html",
            context=context,
        )

        return HttpResponse(html, content_type="text/html")


class EmployeeTreeAPI(APIView):
    permission_classes = [IsAuthenticated]

    employee_id = openapi.Parameter(
        "employee_id",
        openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        required=False,
    )

    department_id = openapi.Parameter(
        "department_id",
        openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        required=False,
    )

    @staticmethod
    def get_children(employee: Employee):
        employees = employee.get_children()
        children = []

        for employee in employees:

            if employee.avatar:
                avatar = get_thumbnail(employee.avatar, '200x200', crop='center', quality=99)
            else:
                config = OrganizationConfig.objects.get()
                avatar = get_thumbnail(config.logo, '200x200', crop='center', quality=99)

            descendants = len(employee.get_descendants())

            try:
                position = employee.position.name
            except AttributeError:
                position = "Не указано"

            try:
                department = employee.department.name
            except AttributeError:
                department = "Не указано"

            employee_data = {
                "id": employee.id,
                "person": {
                    "id": employee.id,
                    "avatar": avatar.url,
                    "department": department,
                    "name": employee.fio,
                    "title":position,
                    "totalReports": descendants,
                    "link": reverse("employees:employee_detail", args=[employee.id]),
                },
                "hasChild": not employee.is_leaf_node(),
                "hasParent": True if descendants > 0 else False,
                "isHighlight": True,
                "children": [],
            }
            children.append(employee_data)
        return children

    def get_employees(self):
        employee_id = self.request.query_params.get("employee_id", None)

        if employee_id is not None:
            employee = Employee.objects.get(id=employee_id)
            return self.get_children(employee)
        else:
            department_id = self.request.query_params.get("department_id", None)
            if department_id is not None:
                department = Department.objects.get(id=department_id)
                employee = department.supervisor

                if not employee:
                    employee = Employee.objects.first().get_root()

            else:
                employee = Employee.objects.first().get_root()

            if employee.avatar:
                avatar = get_thumbnail(employee.avatar, '200x200', crop='center', quality=99)
            else:
                config = OrganizationConfig.objects.get()
                avatar = get_thumbnail(config.logo, '200x200', crop='center', quality=99)

            descendants = len(employee.get_descendants())

            try:
                position = employee.position.name
            except AttributeError:
                position = "Не указано"

            try:
                department = employee.department.name
            except AttributeError:
                department = "Не указано"

            employee_data = {
                "id": employee.id,
                "person": {
                    "id": employee.id,
                    "avatar": avatar.url,
                    "department": department,
                    "name": employee.fio,
                    "title": position,
                    "totalReports": descendants,
                    "link": reverse("employees:employee_detail", args=[employee.id]),
                },
                "hasChild": not employee.is_leaf_node(),
                "hasParent": True if descendants > 0 else False,
                "isHighlight": True,
                "children": self.get_children(employee)
            }
            return employee_data

    @swagger_auto_schema(
        manual_parameters=[
            employee_id,
            department_id,
        ],
    )
    def get(self, request, *args, **kwargs):
        employees = self.get_employees()
        return Response(data=employees, status=status.HTTP_200_OK)