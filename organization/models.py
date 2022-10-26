from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Filial(models.Model):
    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    name = models.CharField("Название", max_length=128)

    def __str__(self):
        return self.name


class Department(MPTTModel):
    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"

    name = models.CharField("Название", max_length=128)
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
