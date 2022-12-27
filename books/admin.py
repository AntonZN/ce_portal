from django.contrib import admin

from utils.forms import TagsAdminForm
from .models import Book, Category


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = TagsAdminForm


admin.site.register(Category)