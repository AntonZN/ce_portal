from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ce_portal.views import HomeView, ProfileView, manage_employee_contacts

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("", include("django.contrib.auth.urls")),
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
    path("organization/", include("organization.urls", namespace="organization")),
    path(
        "organization/employees/",
        include("organization.employees.urls", namespace="employees"),
    ),
    path("blog/", include("blog.urls"), name="news"),
    path("editorjs/", include("django_editorjs_fields.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
