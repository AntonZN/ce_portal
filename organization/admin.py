from django.contrib import admin
from django.contrib.admin import display
from mptt.admin import DraggableMPTTAdmin
from sorl.thumbnail.admin import AdminImageMixin

from .models import Department, Filial, OrganizationConfig, PhraseForHomePage, PhraseDay, Banner, City
from solo.admin import SingletonModelAdmin


@admin.register(Department)
class DepartmentAdmin(DraggableMPTTAdmin):
    search_fields = ("name",)


class PhraseForHomeInline(admin.TabularInline):
    extra = 0
    model = PhraseForHomePage


class BannerAdminInline(AdminImageMixin, admin.StackedInline):
    extra = 0
    model = Banner


@admin.register(OrganizationConfig)
class OrganizationConfigAdmin(AdminImageMixin, SingletonModelAdmin):
    inlines = (PhraseForHomeInline, BannerAdminInline)


@admin.register(PhraseDay)
class PhraseDayAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "get_likes")
    ordering = ("name",)

    @display(description='Оценок')
    def get_likes(self, obj):
        return obj.likes.count()


admin.site.register(City)
