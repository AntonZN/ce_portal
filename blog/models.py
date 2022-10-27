from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_editorjs_fields import EditorJsJSONField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager

from blog.utils import count_words, read_time


class Category(MPTTModel):
    parent = TreeForeignKey(
        "self",
        verbose_name="Родительская категория",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField("Название", max_length=100, null=False, blank=False)
    slug = AutoSlugField("Название для ulr", populate_from="name")
    image = ImageField(upload_to="images/posts/category", blank=True, null=True)
    approved = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category_posts", kwargs={"slug": self.slug})


class Post(models.Model):

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
    title = models.CharField("Заголовок", max_length=250, null=False, blank=False)
    slug = AutoSlugField("Название для ulr", populate_from="title")
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
    views = models.PositiveIntegerField("Кол-во просмотров", default=0)
    count_words = models.CharField("Всего слов", max_length=50, default=0)
    read_time = models.CharField("Время чтения", max_length=50, default=0)

    date_created = models.DateTimeField("Создание", auto_now_add=True)
    date_updated = models.DateTimeField("Обновление", auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.count_words = count_words(self.body)
        self.read_time = read_time(self.body)
        super(Post, self).save(*args, **kwargs)


class News(Post):
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news",
    )

    tags = TaggableManager(blank=True)
    date_published = models.DateTimeField(
        "Дата публикации",
        help_text="Дата и время после которой публикация станет доступной для чтения",
        null=True,
        blank=True,
        default=timezone.now,
    )
    home_view = models.BooleanField("Отображать на главной", default=True)
    main_image = ImageField(
        upload_to="images/posts",
        verbose_name="Заглавное изображение",
        help_text="Изображение в формате jpg, с соотношением сторон 16:9, рекомендуемое разрещение 1400x400",
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return reverse(
            "blog:news_detail",
            kwargs={"slug": self.slug},
        )
