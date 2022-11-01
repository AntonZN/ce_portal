from django.urls import path

from organization.employees.views import EmployeeDetail, EmployeeList

app_name = "employees"

# article/urls.py
urlpatterns = [
    path(route="", view=EmployeeList.as_view(), name="employee_list"),
    path(route="<int:pk>/", view=EmployeeDetail.as_view(), name="employee_detail"),
]