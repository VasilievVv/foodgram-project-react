from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from .validators import UsernameValidator


class MyUserManager(UserManager):
    """
    Кастомный менеджер для модели User.
    """

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Создает юзера.
        """
        return super().create_user(
            username,
            email,
            password,
            **extra_fields
        )

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Создает суперюзера.
        """
        extra_fields.setdefault('role', 'admin')
        return super().create_superuser(
            username,
            email,
            password,
            **extra_fields
        )


class User(AbstractUser):
    """
    Кастомная модель User.
    """
    GUEST = 'guest'
    USER = 'user'
    ADMIN = 'admin'
    ROLES = (
        (GUEST, GUEST),
        (USER, USER),
        (ADMIN, ADMIN),
    )

    username = models.CharField(
        'пользователь',
        max_length=150,
        unique=True,
        validators=[UsernameValidator()],
    )
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField('имя', max_length=150)
    last_name = models.CharField('фамилия', max_length=150)
    role = models.CharField(
        'Role',
        max_length=9,
        choices=ROLES,
        default='user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name', ]

    objects = MyUserManager()

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    @property
    def is_guest(self):
        return self.role == self.GUEST

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
    )
    is_subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_subscribed',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'is_subscribed'],
                name='unique_is_subscribed'),
            models.CheckConstraint(
                check=~models.Q(is_subscribed=models.F('user')),
                name='cant_subscribe_yourself'
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f"Подписка пользователя {self.user} на автора {self.is_subscribed}"
