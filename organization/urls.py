from django.urls import path, include
from django.views.generic import TemplateView

app_name = "organization"

urlpatterns = [

    path(
        "departments/",
        TemplateView.as_view(template_name="organization/departments/tree.html"),
        name="departments"
    ),
    path(
        "api/v1/",
        include("organization.employees.api.urls"),
    ),
    path(
        "api/v1/",
        include("organization.api.urls"),
    ),
]
