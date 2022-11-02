from datetime import timedelta

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.middleware.csrf import get_token

from rest_framework.views import APIView

from organization.employees.api.serializers import EmployeeSearchSerializer
from organization.employees.models import EmployeeLikes, Employee


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
