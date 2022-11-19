from .v1 import *

from django.urls import path

urlpatterns = [
    path(route="phrase/like/<int:phrase_id>/", view=LikePhrase.as_view(), name="phrase_like"),
    path(route="departments/tree/", view=DepartmentTreeAPI.as_view(), name="departments_tree"),
    path(route="filials/", view=FilialsView.as_view(), name="filial_list"),
]
