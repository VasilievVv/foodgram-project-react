from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Описываем модель юзера в админке."""

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_editable = (
        'first_name',
        'last_name',
    )
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email',)
    ordering = ('id',)
    empty_value_display = '-пусто-'


admin.site.unregister(Group)
