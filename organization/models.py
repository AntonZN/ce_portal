from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from solo.models import SingletonModel
from sorl.thumbnail import ImageField


class OrganizationConfig(SingletonModel):
    org_name = models.CharField(
        "Название организации", max_length=255, default="Название организации"
    )
    logo = ImageField(upload_to="org", verbose_name="Логотип", blank=True, null=True)
    description = models.TextField("Описание", null=True)

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


class Department(MPTTModel):
    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "3. Департаменты"

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


class PhraseDay(models.Model):
    name = models.TextField("Фраза")
    created = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Фраза дня"
        verbose_name_plural = "4. Фразы дня"

    def __str__(self):
        return self.name


class PhraseDayLikes(models.Model):
    employee = models.ForeignKey("employees.Employee", on_delete=models.CASCADE, related_name="+")
    phrase = models.ForeignKey(PhraseDay, on_delete=models.CASCADE, related_name="likes")


class PhraseForHomePage(models.Model):
    phrase = models.ForeignKey(PhraseDay, verbose_name="Фраза дня", on_delete=models.CASCADE, related_name="+")
    conf = models.ForeignKey(OrganizationConfig, on_delete=models.CASCADE, related_name="phrases")

    class Meta:
        verbose_name = "Фраза дня"
        verbose_name_plural = "Фразы которые отображать на Главной Странице"

    def __str__(self):
        return ""
