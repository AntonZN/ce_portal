from autoslug import AutoSlugField
from django.db import models
from filer.fields.image import FilerImageField, FilerFileField


class Category(models.Model):
    name = models.CharField("Название", max_length=100, null=False, blank=False)
    slug = AutoSlugField("Название для ulr", populate_from="name")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField("Название", max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="books"
    )
    author = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Автор"
    )
    description = models.TextField(
        max_length=500, null=True, blank=True, verbose_name="Описание"
    )
    file = FilerFileField(related_name="book_file", on_delete=models.CASCADE, verbose_name="Файл книги")
    cover = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="book_image",
        verbose_name="Обложка",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["name"]
