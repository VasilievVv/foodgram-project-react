from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    """
    Кастомная модель администратора
    """
    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",)
    list_filter = ("username", "email",)
    search_fields = ("username", "email",)


admin.site.register(CustomUser, CustomUserAdmin)
