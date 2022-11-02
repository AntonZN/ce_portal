from .v1 import *

from django.urls import path


urlpatterns = [
    path(route="search/", view=EmployeeSearch.as_view(), name="employee-search"),
    path(route="like/<int:employee_id>/", view=LikeEmployee.as_view(), name="employee_like"),
]
