from django.contrib.auth import get_user_model
from django_filters import rest_framework

from .models import Recipe, Tag

User = get_user_model()


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр для модели Рецепта."""

    author = rest_framework.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='author',
    )
    # is_favorited =
    # is_in_shopping_cart =
    tags = rest_framework.ModelChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
    )

    class Meta:
        model = Recipe
        fields = ('author',
                  # 'is_favorited',
                  # 'is_in_shopping_cart',
                  'tags', )

    def get_is_favorited(self):
        pass

    def get_is_in_shopping_cart(self):
        pass