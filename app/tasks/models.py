from django.db import models
from django.contrib.auth.models import User

from .utils import generate_pk


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram ID",
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} (Telegram ID: {self.telegram_id})"


class Category(models.Model):
    id = models.CharField(
        primary_key=True,
        default=generate_pk,
        editable=False,
        max_length=16,
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Пользователь",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Task(models.Model):
    id = models.CharField(
        primary_key=True,
        default=generate_pk,
        editable=False,
        max_length=16,
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )
    due_date = models.DateTimeField(
        verbose_name="Дата выполнения",
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Пользователь",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Категория",
    )
    is_done = models.BooleanField(
        default=False,
        verbose_name="Завершена",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
