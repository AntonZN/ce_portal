from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from blog.models import News, Category
from utils.admin import copy_action
from utils.forms import TagsAdminForm

admin.site.register(Category)


@admin.register(News)
class NewsAdmin(AdminImageMixin, admin.ModelAdmin):
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "category",
                    "title",
                    "slug",
                    "description",
                    "main_image",
                    "body",
                )
            },
        ),
        (
            "Публикация",
            {
                "fields": (
                    "status",
                    "date_published",
                    "date_created",
                    "date_updated",
                )
            },
        ),
        (
            "Отображение",
            {"fields": ("home_view",)},
        ),
    )

    list_display = (
        "title",
        "date_created",
        "status",
        "views",
        "count_words",
        "read_time",
    )
    list_display_links = ("title",)
    search_fields = ("title", "body")
    list_editable = ("status",)
    list_filter = (
        "status",
        "date_published",
        "author",
    )
    date_hierarchy = "date_published"
    ordering = [
        "status",
        "-date_created",
    ]
    readonly_fields = (
        "slug",
        "views",
        "count_words",
        "read_time",
        "date_created",
        "date_updated",
    )
    show_full_result_count = True
    list_per_page = 10
    list_max_show_all = 100
    list_select_related = True
    actions = (copy_action,)
    form = TagsAdminForm

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
