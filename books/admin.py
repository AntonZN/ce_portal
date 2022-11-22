from django.contrib import admin

from utils.forms import TagsAdminForm
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = TagsAdminForm
