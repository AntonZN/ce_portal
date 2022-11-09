from django.urls import path, include

app_name = "organization"

urlpatterns = [
    path(
        "api/v1/emloyees/",
        include("organization.employees.api.urls"),
    ),
    path(
        "api/v1/ogranization/",
        include("organization.api.urls"),
    ),
]
