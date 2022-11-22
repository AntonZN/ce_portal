from django.urls import path
from .views import BooksList

app_name = "books"

urlpatterns = [
    path(route="books/", view=BooksList.as_view(), name="book_list"),
]
