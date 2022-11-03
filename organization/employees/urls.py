from django.urls import path

from organization.employees.views import EmployeeDetail, EmployeeList
from organization.views import AwardList, AwardDetail

app_name = "employees"

urlpatterns = [
    path(route="", view=EmployeeList.as_view(), name="employee_list"),
    path(route="<int:pk>/", view=EmployeeDetail.as_view(), name="employee_detail"),
    path(route="awards/", view=AwardList.as_view(), name="awards_list"),
    path(route="awards/<int:pk>/", view=AwardDetail.as_view(), name="awards_detail"),
]