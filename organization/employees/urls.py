from django.urls import path

from organization.employees.views import EmployeeDetail

app_name = "employees"

# article/urls.py
urlpatterns = [
    # path(route="", view=NewsListView.as_view(), name="employee_list"),
    path(route="<int:employee_id>", view=EmployeeDetail.as_view(), name="employee_detail"),
]