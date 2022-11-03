from django.conf import settings
from django.db import models
from django_editorjs_fields import EditorJsJSONField


class Event(models.Model):

    DRAFTED = "DRAFTED"
    PUBLISHED = "PUBLISHED"

    STATUS_CHOICES = (
        (DRAFTED, "Черновик"),
        (PUBLISHED, "Опубликовано"),
    )

    class Meta:
        abstract = True

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )

    description = models.TextField("Краткое описание", null=False, blank=False)
    body = EditorJsJSONField(
        hideToolbar=False,
        inlineToolbar=False,
        autofocus=True,
        i18n=settings.EDITOR_I18N,
        placeholder="Напишите что-нибудь...",
        verbose_name="Контент",
        null=True,
        blank=True,
    )

    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default=DRAFTED
    )
