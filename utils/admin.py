from uuid import uuid4

from django.contrib import admin


@admin.action(description="Копировать выбранное")
def copy_action(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None
        obj.save()


@admin.action(description="Копировать выбранное")
def copy_user_action(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None
        obj.username = str(uuid4())
        obj.email = f"{uuid4()}@mail.ru"
        obj.save()
