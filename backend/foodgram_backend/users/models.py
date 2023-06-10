# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# class CustomUser(AbstractUser):
#     """
#     Кастомная модель пользователя.
#     """
#
#     email = models.EmailField(
#         'email',
#         unique=True,
#         max_length=254,
#     )
#     username = models.CharField(
#         'username',
#         unique=True,
#         max_length=150,
#     )
#
#     class Meta:
#         ordering = ['username']
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']
#
#     def __str__(self):
#         return self.username

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None,
                         **kwargs,
                         ):
        user = self.create_user(
            email,
            password=password,
            **kwargs,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        'email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        'пользователь',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField('имя', max_length=50)
    last_name = models.CharField('фамилия', max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin