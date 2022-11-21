from django.conf import settings
from django.db import models
from colorfield.fields import ColorField
from sorl.thumbnail import ImageField


class Choices(models.Model):
    choice = models.CharField("Ответ", max_length=5000)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.choice

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "3. Варианты ответа"


class Questions(models.Model):
    NO_MULTIPLE = "multiple choice"
    CHECKBOX = "checkbox"
    SHORT = "short"
    PARAGRAPH = "paragraph"

    QUESTIONS_TYPE_CHOICES = (
        (NO_MULTIPLE, "Один из списка"),
        (CHECKBOX, "Несколько из списка"),
        (SHORT, "Крактий ответ"),
        (PARAGRAPH, "Развернутый ответ"),
    )

    question = models.CharField(max_length=10000, verbose_name="Вопрос")
    question_type = models.CharField(
        max_length=20,
        choices=QUESTIONS_TYPE_CHOICES,
        default=NO_MULTIPLE,
        verbose_name="Тип вопроса",
    )
    required = models.BooleanField(default=False, verbose_name="Обязательный")
    answer_key = models.CharField(
        max_length=5000, blank=True, verbose_name="Ключ ответа"
    )
    score = models.IntegerField(blank=True, default=0, verbose_name="Баллы")
    feedback = models.CharField(
        max_length=5000, null=True, blank=True, verbose_name="Обратная связь"
    )
    choices = models.ManyToManyField(
        Choices, related_name="choices", verbose_name="Варианты ответа"
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "2. Вопросы"


class Answer(models.Model):
    answer = models.CharField(max_length=5000, verbose_name="Ответ")
    answer_to = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
        related_name="answer_to",
        verbose_name="Вопрос",
    )

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Form(models.Model):
    code = models.CharField(max_length=30, verbose_name="Код формы")
    title = models.CharField("Заголовок", max_length=200)
    description = models.TextField(
        verbose_name="Описание", max_length=10000, blank=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="creator",
    )
    background_color = ColorField(
        default="#f9f8f9", verbose_name="Цвет фона"
    )
    text_color = ColorField(
        default="#222", verbose_name="Цвет текста"
    )
    collect_email = models.BooleanField(default=False, verbose_name="Сбор почты")
    authenticated_responder = models.BooleanField(
        default=True, verbose_name="Только зарегистрированные пользователи"
    )
    edit_after_submit = models.BooleanField(
        default=False, verbose_name="Редактирование после отправки"
    )
    confirmation_message = models.CharField(
        max_length=10000,
        default="Спасибо за участие!",
        verbose_name="Сообщение после прохождения",
    )
    is_quiz = models.BooleanField(default=False, verbose_name="Квиз")
    allow_view_score = models.BooleanField(
        default=True, verbose_name="Показывать результаты"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    questions = models.ManyToManyField(
        Questions, related_name="questions", verbose_name="Вопросы",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Форма опроса"
        verbose_name_plural = "1. Формы"


class Responses(models.Model):
    response_code = models.CharField(max_length=20, verbose_name="Код ответа")
    response_to = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="response_to", verbose_name="Форма"
    )
    responder_ip = models.CharField(max_length=30, verbose_name="IP адрес")
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="responder",
        blank=True,
        null=True,
        verbose_name="Ответивший",
    )
    responder_email = models.EmailField(blank=True, verbose_name="Почта")
    response = models.ManyToManyField(
        Answer, related_name="response", verbose_name="Ответы"
    )
