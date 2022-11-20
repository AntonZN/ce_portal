from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin
from mptt.admin import DraggableMPTTAdmin
from sorl.thumbnail.admin import AdminImageMixin

from utils.admin import copy_user_action
from utils.forms import TagsAdminForm
from .models import Employee, Position, Contacts, Awards, EmployeeAwards

admin.site.register(Position)


class EmployeeAwardsInline(TabularInline):
    model = EmployeeAwards
    extra = 0
    can_delete = False
    show_change_link = False
    autocomplete_fields = ("employee",)


class ContactsInline(AdminImageMixin, TabularInline):
    model = Contacts
    can_delete = False
    show_change_link = False
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(AdminImageMixin, UserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Персональная информация", {"fields": ("fio", "email", "birthday", "avatar")}),
        ("Штатная информация", {"fields": ("department", "parent", "position")}),
        ("Прочая информация", {"fields": ("description",)}),
        (
            "Привилегии",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("fio", "username", "email", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "fio", "email", "parent", "is_staff")
    list_display_links = ("username",)
    search_fields = ("fio", "username", "email")
    autocomplete_fields = ("parent", "department")
    readonly_fields = ("last_login", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "department", "position")
    inlines = (ContactsInline,)
    actions = (copy_user_action,)
    form = TagsAdminForm

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return self.readonly_fields + ("is_active", "is_staff", "is_superuser")
        return self.readonly_fields


@admin.register(Awards)
class AwardsAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = (EmployeeAwardsInline,)
