from django.conf import settings
from django.db import models


class FeedbackCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    name = models.CharField("Название", max_length=256)

    def __str__(self):
        return self.name


class BaseFeedback(models.Model):
    CREATED = "CREATED"
    RESOLVED = "RESOLVED"

    STATUS_CHOICES = (
        (CREATED, "Создано"),
        (RESOLVED, "Обработано"),
    )

    topic = models.CharField(max_length=512, verbose_name="Тема")

    text = models.TextField("Обращение")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="от Сотрудника",
    )

    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default=CREATED
    )

    created = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.topic


class Feedback(BaseFeedback):
    QUESTION = "QUESTION"
    REVIEW = "REVIEW"
    IDEA = "IDEA"

    TYPE_CHOICES = (
        (QUESTION, "Вопрос"),
        (REVIEW, "Отзыв"),
        (IDEA, "Идея"),
    )

    type = models.CharField(
        "Тип обращения", max_length=20, choices=TYPE_CHOICES, default=QUESTION
    )

    # answer = models.TextField("Ответ на обращение", blank=True, null=True)

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "1. Обращения"


class FeedbackForDirector(BaseFeedback):
    class Meta:
        verbose_name = "Вопрос директору"
        verbose_name_plural = "2. Вопросы Директору"
