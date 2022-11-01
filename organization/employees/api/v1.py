from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

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
        # EmployeeLikes.objects.get_or_create(employee_id=employee_id, user=request.user)
        print(1)
        return Response(status=status.HTTP_200_OK)
