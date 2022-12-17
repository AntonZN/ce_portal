from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django_editorjs_fields import EditorJsJSONField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from solo.models import SingletonModel
from sorl.thumbnail import ImageField
from filer.models import Folder


class OrganizationConfig(SingletonModel):
    org_name = models.CharField(
        "Название организации", max_length=255, default="Название организации"
    )
    logo = ImageField(upload_to="org", verbose_name="Логотип", blank=True, null=True)
    description = EditorJsJSONField(
        hideToolbar=False,
        inlineToolbar=True,
        autofocus=True,
        i18n=settings.EDITOR_I18N,
        placeholder="Напишите что-нибудь...",
        verbose_name="О компании",
        null=True,
        blank=True,
    )
    default_img = ImageField(
        upload_to="org",
        verbose_name="Заглушка",
        help_text="Изображение которое используется если у объекта оно не установлено",
        blank=True,
        null=True,
    )
    feedback_email = models.EmailField(
        "Почта на которую отправлять обращения", null=True, blank=True
    )
    director_feedback_email = models.EmailField(
        "Почта на которую отправлять обращения директору", null=True, blank=True
    )
    albums_folder = models.OneToOneField(
        Folder,
        verbose_name="Папка для фотоальбомов",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    knowledge_base = models.OneToOneField(
        Folder,
        verbose_name="Папка для базы знаний",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def __str__(self):
        return "Настройка Организации"

    class Meta:
        verbose_name = "1. Настройка"


class Filial(models.Model):
    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "2. Филиалы"

    name = models.CharField("Название", max_length=128)

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "2. Города"

    name = models.CharField("Название", max_length=128)

    def __str__(self):
        return self.name


class Department(MPTTModel):
    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "3. Департаменты"

    name = models.CharField("Название", max_length=128)
    description = EditorJsJSONField(
        plugins=settings.PLUGINS,
        tools=settings.EDITORJS_CONFIG_TOOLS,
        hideToolbar=False,
        inlineToolbar=True,
        autofocus=True,
        i18n=settings.EDITOR_I18N,
        placeholder="Напишите что-нибудь...",
        verbose_name="Описание",
        null=True,
        blank=True,
    )
    parent = TreeForeignKey(
        "self",
        verbose_name="Вышестоящий департамент",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    supervisor = models.ForeignKey(
        "employees.Employee",
        verbose_name="Руководитель Департамента",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departments",
    )
    filial = models.ForeignKey(
        "Filial",
        verbose_name="Филиал",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departments",
    )

    def __str__(self):
        try:
            return f"{self.name} ({self.filial.name})"
        except AttributeError:
            return self.name


class PhraseDay(models.Model):
    name = models.TextField("Фраза")
    created = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Фраза дня"
        verbose_name_plural = "4. Фразы дня"

    def __str__(self):
        return self.name


class PhraseDayLikes(models.Model):
    employee = models.ForeignKey(
        "employees.Employee", on_delete=models.CASCADE, related_name="+"
    )
    phrase = models.ForeignKey(
        PhraseDay, on_delete=models.CASCADE, related_name="likes"
    )


class PhraseForHomePage(models.Model):
    phrase = models.ForeignKey(
        PhraseDay, verbose_name="Фраза дня", on_delete=models.CASCADE, related_name="+"
    )
    conf = models.ForeignKey(
        OrganizationConfig, on_delete=models.CASCADE, related_name="phrases"
    )

    class Meta:
        verbose_name = "Фраза дня"
        verbose_name_plural = "Фразы которые отображать на Главной Странице"

    def __str__(self):
        return ""


class Banner(models.Model):
    ALL = "ALL"
    IMAGE = "IMAGE"
    TEXT = "TEXT"

    TYPE_CHOICES = (
        (ALL, "Изображение + текст"),
        (IMAGE, "Только Изображение"),
        (TEXT, "Только Текст"),
    )
    type = models.CharField(
        "Тип баннера", max_length=20, choices=TYPE_CHOICES, default=ALL
    )
    title = models.CharField(
        "Заголовок",
        help_text="Обязательно если выбран тип Изображение + текст или Текст",
        blank=True,
        null=True,
        max_length=256,
    )
    description = models.TextField(
        "Подробности",
        help_text="Обязательно если выбран тип Изображение + текст или Текст",
        blank=True,
        null=True,
    )
    link = models.URLField(
        "Ссылка",
        blank=True,
        help_text="Укажите ссылку, если необходимо, в банере появится кнопка подробнее",
        null=True,
    )
    image = ImageField(
        "Изображение",
        upload_to="banners",
        help_text="Обязательно если указан тип Изображение + текст или Изображение",
        blank=True,
        null=True,
    )
    background_color = ColorField(
        default="#f9f8f9",
        verbose_name="Цвет фона",
        blank=True,
        null=True,
        help_text="Выберите цвет, если указан тип - Текст",
    )
    order = models.PositiveIntegerField("Порядок сортировки", default=0)
    is_view = models.BooleanField("Отображать в слайдере?", default=True)
    conf = models.ForeignKey(
        OrganizationConfig, on_delete=models.CASCADE, related_name="banners"
    )

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннера"

    def __str__(self):
        return ""
