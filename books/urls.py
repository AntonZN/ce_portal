from django.urls import path
from .views import BooksList, BookDetail

app_name = "books"

urlpatterns = [
    path(route="", view=BooksList.as_view(), name="book_list"),
    path(route="<int:pk>/", view=BookDetail.as_view(), name="book_detail"),
    path(route="cetegory/<slug:slug>/", view=BooksList.as_view(), name="book_category_list"),
]
