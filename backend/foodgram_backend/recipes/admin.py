from django.contrib import admin

from .models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, RecipeIngredients


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Описываем модель Тег в админке."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'color', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Описываем модель Ингридиента в админке."""

    list_display = ('id', 'name', 'measurement_unit', )
    search_fields = ('name', )
    list_filter = ('name', )
    ordering = ('id', )
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredients)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount', )
    list_editable = ('amount', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Описываем модель Рецепта в админке."""

    list_display = ('id', 'name', 'image', 'author', )
    search_fields = ('name', 'author', )
    list_filter = ('name', 'author', )
    filter_horizontal = ('tags', )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Описываем модель Избранного в админке."""

    list_display = ('id', 'recipe', 'user')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Описываем модель Списка покупок в админке."""

    list_display = ('id', 'recipe', 'user')
    empty_value_display = '-пусто-'
