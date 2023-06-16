from rest_framework.serializers import ModelSerializer

from .models import Tag, Ingredient, Recipe


class TagSerializer(ModelSerializer):
    """Сериализатор для Tag."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(ModelSerializer):
    """Сериализатор для Ingredient."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class FavoriteSerializer(ModelSerializer):
    """Сериализатор для Избранного."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time') # 'image' добавить


class ShoppingCartSerializer(ModelSerializer):
    """Сериализатор для Списка покупок."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time') # 'image' добавить
