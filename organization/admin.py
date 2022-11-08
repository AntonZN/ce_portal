from django.contrib import admin
from django.contrib.admin import display

from .models import Department, Filial, OrganizationConfig, PhraseForHomePage, PhraseDay
from solo.admin import SingletonModelAdmin


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class PhraseForHomeInline(admin.TabularInline):
    extra = 0
    model = PhraseForHomePage


@admin.register(OrganizationConfig)
class OrganizationConfigAdmin(SingletonModelAdmin):
    inlines = (PhraseForHomeInline,)


@admin.register(PhraseDay)
class PhraseDayAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "get_likes")

    @display(description='Оценок')
    def get_likes(self, obj):
        return obj.likes.count()


admin.site.register(Filial)
