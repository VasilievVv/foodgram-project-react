from django.contrib import admin

from .models import Tag, Ingredient, Recipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Описываем модель Тег в админке."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'color', 'slug', )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Описываем модель Ингридиента в админке."""

    list_display = ('id', 'name', 'amount', 'measurement_unit', )
    list_editable = ('name', 'amount', 'measurement_unit', )
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Описываем модель Рецепта в админке."""

    empty_value_display = '-пусто-'