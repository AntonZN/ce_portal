from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin
from mptt.admin import DraggableMPTTAdmin
from sorl.thumbnail.admin import AdminImageMixin

from utils.admin import copy_user_action
from utils.forms import TagsAdminForm, UserAdminForm
from .models import (
    Employee,
    Position,
    Contacts,
    Awards,
    EmployeeAwards,
    EmployeeAdditionalPosition,
)


@admin.register(Position)
class PositionAdmin(AdminImageMixin, admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


class EmployeeAdditionalPositionInline(TabularInline):
    model = EmployeeAdditionalPosition
    extra = 0
    show_change_link = False
    autocomplete_fields = ("position", "department")


class EmployeeAwardsInline(TabularInline):
    model = EmployeeAwards
    extra = 0
    can_delete = False
    show_change_link = False
    autocomplete_fields = ("employee",)


class ContactsInline(AdminImageMixin, TabularInline):
    model = Contacts
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(AdminImageMixin, UserAdmin, DraggableMPTTAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password", "tree_root")}),
        ("Персональная информация", {"fields": ("fio", "email", "birthday", "avatar")}),
        (
            "Штатная информация",
            {
                "fields": (
                    "city",
                    "department",
                    "parent",
                    "position",
                    "internal_phone",
                    "mobile_phone",
                )
            },
        ),
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
                "fields": (
                    "fio",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "parent",
                    "department",
                ),
            },
        ),
    )
    list_display = (
        "tree_actions",
        "indented_title",
        "username",
        "email",
        "parent",
        "is_staff",
    )
    list_display_links = ("indented_title",)
    mptt_indent_field = "indented_title"
    search_fields = ("fio", "username", "email")
    autocomplete_fields = ("parent", "department")
    readonly_fields = ("last_login", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "department", "position")
    inlines = (ContactsInline, EmployeeAdditionalPositionInline)
    actions = (copy_user_action,)
    form = UserAdminForm

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return self.readonly_fields + ("is_active", "is_staff", "is_superuser")
        if Employee.objects.filter(tree_root=True).exists() and not obj.tree_root:
            return self.readonly_fields + ("tree_root",)
        return self.readonly_fields


@admin.register(Awards)
class AwardsAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = (EmployeeAwardsInline,)
    ordering = ("name",)
