from datetime import timedelta

from django.db.models import Q, F
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import get_token
from rest_framework.response import Response

from rest_framework.views import APIView
from sorl.thumbnail import get_thumbnail

from blog.models import News
from organization.employees.api.serializers import (
    FilialSerializer,
    DepartmentSerializer,
)
from organization.employees.models import Employee
from organization.models import (
    PhraseDay,
    PhraseDayLikes,
    OrganizationConfig,
    Department,
    Filial,
)


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

        if PhraseDayLikes.objects.filter(employee=request.user, phrase=phrase).exists():
            context["htmx_message"] = "Вы уже голосовали за эту фразу"
        else:
            PhraseDayLikes.objects.create(employee=request.user, phrase=phrase)
            context["htmx_message"] = "Голос успешно засчитан"

        html = render_to_string(
            template_name="other/phrase_like.html",
            context=context,
        )

        return HttpResponse(html, content_type="text/html")


class FilialsView(generics.ListAPIView):
    serializer_class = FilialSerializer
    queryset = Filial.objects.all()


class DepartmentsView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


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

        for department in departments:

            try:
                avatar = get_thumbnail(
                    department.supervisor.avatar, "200x200", crop="center", quality=99
                )
            except Exception:
                avatar = get_thumbnail(
                    config.logo, "200x200", crop="center", quality=99
                )

            if department.filial:
                title = department.filial.name
            else:
                title = ""

            employee_data = {
                "id": department.id,
                "person": {
                    "id": department.id,
                    "avatar": avatar.url,
                    "name": department.name,
                    "title": title,
                    "totalReports": department.get_children().count(),
                    "link": reverse(
                        "organization:department_detail", args=[department.id]
                    ),
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

            try:
                avatar = get_thumbnail(
                    department.supervisor.avatar, "200x200", crop="center", quality=99
                )
            except Exception:
                avatar = get_thumbnail(
                    config.logo, "200x200", crop="center", quality=99
                )

            if department.filial:
                title = department.filial.name
            else:
                title = ""

            employee_data = {
                "id": department.id,
                "person": {
                    "id": department.id,
                    "avatar": avatar.url,
                    "name": department.name,
                    "title": title,
                    "totalReports": department.get_children().count(),
                    "link": reverse(
                        "organization:department_detail", args=[department.id]
                    ),
                },
                "hasChild": not department.is_leaf_node(),
                "hasParent": department.is_child_node(),
                "isHighlight": True,
                "children": self.get_children(department),
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


def get_news(query):

    return (
        [news.get_search_data() for news in News.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__name__in=[query])
        ).distinct()]
    )


def get_employees(query):

    return (
        [employee.get_search_data() for employee in Employee.objects.filter(
            Q(fio__icontains=query)
            | Q(username__icontains=query)
            | Q(position__name__icontains=query)
            | Q(department__name__icontains=query)
            | Q(tags__name__in=[query])
        ).distinct()]
    )


class Search(APIView):
    permission_classes = [IsAuthenticated]

    query = openapi.Parameter(
        "query",
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=False,
    )

    @swagger_auto_schema(
        manual_parameters=[
            query,
        ],
    )
    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)

        if query:
            query = query.strip()
            query = query.replace("#", "")
            employees = get_employees(query)
            news = get_news(query)
            data_list = employees + news
            return Response(data=data_list, status=status.HTTP_200_OK)
        else:
            return Response(data=[], status=status.HTTP_200_OK)

