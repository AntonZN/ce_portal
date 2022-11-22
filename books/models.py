from django.db import models
from filer.fields.image import FilerImageField, FilerFileField


class Book(models.Model):
    name = models.CharField("Название", max_length=200)
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
