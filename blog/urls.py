from django.urls import path
from .views import NewsListView

app_name = "blog"

# article/urls.py
urlpatterns = [
    path(route="news", view=NewsListView.as_view(), name="news_list"),
]