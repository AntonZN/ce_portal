from django.urls import path, include

app_name = "blog"

# article/urls.py
urlpatterns = [
    path(
        "api/v1/emloyees/",
        include("organization.employees.api.urls"),
    ),
    # path(route="", view=NewsListView.as_view(), name="news_list"),
]
