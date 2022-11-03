from django.urls import path
from .views import NewsList, NewsDetail

app_name = "blog"

urlpatterns = [
    path(route="news", view=NewsList.as_view(), name="news_list"),
    path(route="news/<slug:slug>/", view=NewsDetail.as_view(), name="news_detail"),
]