from django.contrib.auth import get_user_model
import django_filters

from .models import Recipe, Tag

User = get_user_model()


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для модели Рецепта."""

    author = django_filters.AllValuesFilter(
        field_name='author__id'
    )
    # is_favorited =
    # is_in_shopping_cart =
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = ('author',
                  # 'is_favorited',
                  # 'is_in_shopping_cart',
                  'tags', )
    #
    # def get_is_favorited(self):
    #     pass
    #
    # def get_is_in_shopping_cart(self):
    #     pass