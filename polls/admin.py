from django.contrib import admin
from django.contrib.admin import display
from django.forms import BaseInlineFormSet, ModelForm
from django import forms
from django.urls import reverse
from django.utils.html import format_html

from .models import *


class QuestionsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['questions'].label = "Вопрос"


class ChoicesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choices'].label = "Ответ"


class FormProxy(Form.questions.through):
    class Meta:
        proxy = True

    def __str__(self):
        return f"№ {self.id}"


class QuestionsInline(admin.TabularInline):
    model = FormProxy
    extra = 0
    verbose_name = "Вопрос"
    verbose_name_plural = "Список вопросов"
    form = QuestionsForm


class QuestionsProxy(Questions.choices.through):
    class Meta:
        proxy = True

    def __str__(self):
        return f"№ {self.id}"


class ChoicesInline(admin.TabularInline):
    model = QuestionsProxy
    extra = 0
    verbose_name = "Ответ"
    verbose_name_plural = "Список ответов"
    form = ChoicesForm


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "created_at", "get_edit_url", "get_result_url")
    fieldsets = (
        ("Основное", {"fields": ("title", "description", "confirmation_message")}),
        ("Оформление", {"fields": ("background_color", "text_color")}),
        ("Даты", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")

    inlines = (QuestionsInline,)

    @display(description="Редактировать")
    def get_edit_url(self, obj):
        url = reverse("polls:edit_form", kwargs=dict(code=obj.code))
        return format_html("<a target='_blank' href='{0}'>Перейти</a>", url)

    @display(description="Результаты")
    def get_result_url(self, obj):
        url = reverse("polls:responses", kwargs=dict(code=obj.code))
        return format_html("<a target='_blank' href='{0}'>Перейти</a>", url)

    get_edit_url.allow_tags = True

    verbose_name = "Форма"
    verbose_name_plural = "Формы"


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    fields = ("question", "question_type", "required")

    inlines = (ChoicesInline,)

    verbose_name = "Вопрос"
    verbose_name_plural = "Список вопросов"


@admin.register(Choices)
class ChoicesAdmin(admin.ModelAdmin):
    fields = ("choice",)

    verbose_name = "Ответ"
    verbose_name_plural = "Список ответов"
