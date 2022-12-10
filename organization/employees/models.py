from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils import timezone
from model_utils.managers import QueryManager
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser

from django.contrib.auth.models import UserManager
from mptt.managers import TreeManager
from sorl.thumbnail import ImageField
from birthday import BirthdayField, BirthdayManager


class EmployeeManager(TreeManager, UserManager, BirthdayManager):
    pass


class Position(models.Model):
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Список дожностей"

    name = models.CharField("Название", max_length=256)

    def __str__(self):
        return self.name


class Contacts(models.Model):
    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контактные данные сотрудника"

    name = models.CharField(
        "Название", help_text="Например: рабочий номер телефона", max_length=256
    )
    value = models.CharField("Значение", max_length=256)
    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="contacts"
    )

    def __str__(self):
        return ""


class Awards(models.Model):
    class Meta:
        verbose_name = "Награду"
        verbose_name_plural = "Награды сотрудников"

    name = models.CharField("Название", max_length=256)
    description = models.TextField("Описание", blank=True, null=True)
    image = ImageField("Изображение", upload_to="awards", null=True, blank=True)

    def get_absolute_url(self):
        return reverse(
            "organization:award_detail",
            kwargs={"pk": self.pk},
        )

    def __str__(self):
        return ""


class EmployeeAwards(models.Model):
    class Meta:
        verbose_name = ""
        verbose_name_plural = "Сотрудники получившие награду"

    employee = models.ForeignKey(
        "Employee",
        verbose_name="Сотрудник",
        on_delete=models.CASCADE,
        related_name="awards",
    )
    award = models.ForeignKey(
        "Awards", on_delete=models.CASCADE, related_name="employees"
    )


class Employee(AbstractUser, MPTTModel):
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Список сотрудников"

    first_name = None
    last_name = None

    email = models.EmailField(
        "Email",
        unique=True,
        blank=True,
        help_text="Email должен быть уникальным, так как будет служить для авторизации сотрудников на портале",
    )
    fio = models.CharField(verbose_name="ФИО", max_length=150, null=True, blank=True)

    parent = TreeForeignKey(
        "self",
        verbose_name="Руководитель",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervisor",
        help_text="Если у сотрудника нет руководителя, оставьте поле пустым",
    )
    birthday = BirthdayField("Дата рождения", null=True, blank=True)
    position = models.ForeignKey(
        "Position",
        verbose_name="Должность",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    department = models.ForeignKey(
        "organization.Department",
        verbose_name="Департамент",
        on_delete=models.SET_NULL,
        related_name="employees",
        max_length=150,
        null=True,
        blank=True,
    )
    description = models.TextField("Информация о сотруднике", blank=True, null=True)
    likes = models.PositiveIntegerField("Лайки", default=0)
    avatar = ImageField("Аватар", upload_to="avatars", null=True, blank=True)
    manager = EmployeeManager()

    new = QueryManager(
        date_joined__gte=timezone.now() - timedelta(days=7)
    ).order_by("-date_joined")

    def __str__(self):
        return f"Сотрудник: {self.fio}"

    def get_search_data(self):
        return {
            "id": self.id,
            "title": self.fio,
            "type": "Cотрудник",
            "url": self.get_absolute_url()
        }

    def get_absolute_url(self):
        return reverse(
            "employees:employee_detail",
            kwargs={"pk": self.id}
        )


class EmployeeLikes(models.Model):
    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="all_likes"
    )
    user = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="+"
    )
    created = models.DateTimeField("Создание", auto_now_add=True)

