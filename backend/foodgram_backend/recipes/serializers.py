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
    """Сериализватор для Избранного."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time') # 'image' добавить
