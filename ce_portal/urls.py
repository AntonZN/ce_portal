from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as get_schema_view_yasg
from rest_framework import permissions

from ce_portal.views import HomeView, ProfileView, manage_employee_contacts

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", HomeView.as_view(), name="home"),
    path("", include("django.contrib.auth.urls")),
    path("", RedirectView.as_view(url='home/', permanent=False)),
    path(
        route="profile/",
        view=ProfileView.as_view(),
        name="profile",
    ),
    path(
        route="profile/contacts/update/",
        view=manage_employee_contacts,
        name="contacts_update",
    ),
    path("polls/", include("polls.urls")),
    path("organization/", include("organization.urls")),
    path(
        "organization/employees/",
        include("organization.employees.urls"),
    ),
    path(
        "feedback/",
        include("feedback.urls"),
    ),
    path("blog/", include("blog.urls")),
    path("editorjs/", include("django_editorjs_fields.urls")),
    path("comments/", include("django_comments.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_url_patterns = [
    path("organization/", include("organization.urls", namespace="organization")),
]

schema_view_yasg = get_schema_view_yasg(
    openapi.Info(
        title="Dozor Manager API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
    patterns=schema_url_patterns,
)

urlpatterns += [
    re_path(
        r"^swagger-rest(?P<format>\.json|\.yaml)$",
        schema_view_yasg.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger-rest/",
        schema_view_yasg.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view_yasg.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
