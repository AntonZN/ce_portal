from django.urls import path
from .views import NewsList, NewsDetail, LikeNews

app_name = "blog"

urlpatterns = [
    path(route="news/", view=NewsList.as_view(), name="news_list"),
    path(route="news/<slug:cat_slug>/", view=NewsList.as_view(), name="news_list"),
    path(route="news/<slug:cat_slug>/<slug:slug>/", view=NewsDetail.as_view(), name="news_detail"),
    path(route="news/<slug:cat_slug>/<slug:slug>/like/", view=LikeNews.as_view(), name="news_like"),
]
