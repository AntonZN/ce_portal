from django.contrib import admin

from .models import Department, Filial


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.register(Filial)
