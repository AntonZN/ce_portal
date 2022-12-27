from django.contrib import admin
from solo.admin import SingletonModelAdmin

# Register your models here.
from .models import *


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("topic", "status", "author", "created")
    list_filter = ("status",)
    readonly_fields = ("author", "created", "text", "topic")


@admin.register(IdeaPage)
class IdeaPageAdmin(SingletonModelAdmin):
    pass


@admin.register(ReleasedEmployeeIdea)
class ReleasedEmployeeIdeaAdmin(admin.ModelAdmin):
    autocomplete_fields = ("employee",)


@admin.register(IdeaFeedback)
class IdeaFeedbackAdmin(admin.ModelAdmin):
    list_display = ("topic", "status", "author", "created")
    readonly_fields = ("author", "created", "text", "topic")


@admin.register(FeedbackForDirector)
class FeedbackForDirectorkAdmin(admin.ModelAdmin):
    list_display = ("topic", "status", "author", "created")
    readonly_fields = ("author", "created", "text", "topic")

