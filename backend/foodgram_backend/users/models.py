from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя
    """

    email = models.EmailField(
        "email",
        unique=True,
        max_length=254,
    )
    username = models.CharField(
        "username",
        unique=True,
        max_length=150,
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password", "first_name", "last_name"]

    def __str__(self) -> str:
        return self.username
