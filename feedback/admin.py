from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("topic", "status", "author", "created")
    list_filter = ("status",)


admin.site.register(FeedbackCategory)