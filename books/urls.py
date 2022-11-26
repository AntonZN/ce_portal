from django.urls import path
from .views import BooksList

app_name = "books"

urlpatterns = [
    path(route="", view=BooksList.as_view(), name="book_list"),
]
