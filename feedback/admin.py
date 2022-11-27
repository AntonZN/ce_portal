from django.contrib import admin
from solo.admin import SingletonModelAdmin

# Register your models here.
from .models import *


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("topic", "status", "author", "created")
    list_filter = ("status",)


@admin.register(IdeaPage)
class IdeaPageAdmin(SingletonModelAdmin):
    pass


@admin.register(ReleasedEmployeeIdea)
class ReleasedEmployeeIdeaAdmin(admin.ModelAdmin):
    autocomplete_fields = ("employee",)


admin.site.register(IdeaFeedback)
admin.site.register(FeedbackForDirector)
