from datetime import timedelta

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import get_token
from rest_framework.response import Response

from rest_framework.views import APIView
from sorl.thumbnail import get_thumbnail

from organization.employees.api.serializers import FilialSerializer
from organization.models import PhraseDay, PhraseDayLikes, OrganizationConfig, Department, Filial


class LikePhrase(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Лайкнуть фразу",
        responses={200: "OK"},
    )
    def post(self, request, phrase_id, *args, **kwargs):
        context = {}

        phrase = PhraseDay.objects.get(id=phrase_id)
        context["phrase"] = phrase
        context["csrf_token"] = get_token(request)

        if PhraseDayLikes.objects.filter(
            employee=request.user, phrase=phrase
        ).exists():
            context["htmx_message"] = "Вы уже голосовали за эту фразу"
        else:
            PhraseDayLikes.objects.create(
                employee=request.user, phrase=phrase
            )
            context["htmx_message"] = "Голос успешно засчитан"

        html = render_to_string(
            template_name="other/phrase_like.html",
            context=context,
        )

        return HttpResponse(html, content_type="text/html")


class FilialsView(generics.ListAPIView):
    serializer_class = FilialSerializer
    queryset = Filial.objects.all()


class DepartmentTreeAPI(APIView):
    # permission_classes = [IsAuthenticated]

    filial_id = openapi.Parameter(
        "filial_id",
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
    def get_children(department):
        departments = department.get_children()
        children = []
        config = OrganizationConfig.objects.get()
        avatar = get_thumbnail(config.logo, '100x100', crop='center', quality=99)

        for department in departments:
            employee_data = {
                "id": department.id,
                "person": {
                    "id": department.id,
                    "avatar": avatar.url,
                    "department": department.filial.name,
                    "name": department.name,
                    "title": department.filial.name,
                    "totalReports": department.get_descendant_count(),
                    # "link": reverse("organization:department_detail", args=[department.id]),
                    "link": "#"
                },
                "hasChild": not department.is_leaf_node(),
                "hasParent": department.is_child_node(),
                "isHighlight": True,
                "children": [],
            }
            children.append(employee_data)
        return children

    def get_departments(self):
        department_id = self.request.query_params.get("department_id", None)

        if department_id is not None:
            department = Department.objects.get(id=department_id)
            return self.get_children(department)
        else:
            filial_id = self.request.query_params.get("filial_id", None)
            if filial_id is not None:
                filial = Filial.objects.get(id=filial_id)
                department = Department.objects.filter(filial=filial).first()
            else:
                department = Department.objects.first().get_root()

            config = OrganizationConfig.objects.get()
            avatar = get_thumbnail(config.logo, '200x200', crop='center', quality=99)

            employee_data = {
                "id": department.id,
                "person": {
                    "id": department.id,
                    "avatar": avatar.url,
                    "department": department.filial.name,
                    "name": department.name,
                    "title": department.filial.name,
                    "totalReports": department.get_descendant_count(),
                    # "link": reverse("organization:department_detail", args=[department.id]),
                    "link": "#"
                },
                "hasChild": not department.is_leaf_node(),
                "hasParent": department.is_child_node(),
                "isHighlight": True,
                "children": self.get_children(department)
            }
            return employee_data

    @swagger_auto_schema(
        manual_parameters=[
            department_id,
            filial_id,
        ],
    )
    def get(self, request, *args, **kwargs):
        employees = self.get_departments()
        return Response(data=employees, status=status.HTTP_200_OK)
