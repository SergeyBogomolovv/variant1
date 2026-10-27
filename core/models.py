from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    username = models.CharField("Логин", unique=True, max_length=150)
    full_name = models.CharField("ФИО", max_length=200)
    phone = models.CharField(
        "Телефон",
        max_length=20,
        validators=[
            RegexValidator(
                r"\A8\(\d{3}\) \d{3}-\d{2}-\d{2}\Z", "Формат: 8(999) 999-99-99"
            )
        ],
    )


class Ticket(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        MEDIUM = "medium", "Средний"
        HIGH = "high", "Высокий"

    class Status(models.TextChoices):
        NEW = "new", "Новое"
        PROGRESS = "progress", "В работе"
        CLOSED = "closed", "Закрыто"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Пользователь",
    )

    topic = models.CharField("Тема", max_length=150)
    description = models.TextField("Описание проблемы")
    desired_date = models.DateField("Желаемая дата решения")
    request_date = models.DateField("Дата обращения", default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField("Приоритет", max_length=10, choices=Priority.choices)
    status = models.CharField(
        "Статус", max_length=10, choices=Status.choices, default=Status.NEW
    )


class Feedback(models.Model):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="feedback",
        verbose_name="Обращение",
    )
    text = models.TextField("Отзыв")
    created_at = models.DateTimeField(auto_now_add=True)
