from .v1 import *

from django.urls import path


urlpatterns = [
    path(route="phrase/like/<int:phrase_id>/", view=LikePhrase.as_view(), name="phrase_like"),
]
