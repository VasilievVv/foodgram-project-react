from django_filters import rest_framework

from .models import Recipe


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр для модели Рецепта."""

    # author =
    # is_favorited =
    # is_in_shopping_cart =
    # tags =

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'is_in_shopping_cart', 'tags', )
