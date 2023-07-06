from django.contrib.auth import get_user_model
import django_filters

from .models import Recipe, Ingredient

User = get_user_model()


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для модели Рецепта."""

    author = django_filters.AllValuesFilter(
        field_name='author__id'
    )
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = ('author',
                  'tags', )


# class IngredientFilter(django_filters.FilterSet):
#     """Фильтр для модели Ингредиентов."""
#
#     name = django_filters.CharFilter(
#         lookup_expr='istartswitch',
#     )
#
#     class Meta:
#         model = Ingredient
#         fields = ('name', )
