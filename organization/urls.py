from django.urls import path, include
from django.views.generic import TemplateView

from ce_portal.views import DepartmentDetail

app_name = "organization"

urlpatterns = [

    path(
        "departments/",
        TemplateView.as_view(template_name="organization/departments/tree.html"),
        name="departments"
    ),
    path(
        "departments/<int:pk>/",
        DepartmentDetail.as_view(),
        name="department_detail"
    ),
    path(
        "api/v1/employees/",
        include("organization.employees.api.urls"),
    ),
    path(
        "api/v1/",
        include("organization.api.urls"),
    ),
]
