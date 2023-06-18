from rest_framework.serializers import ModelSerializer

from .models import Tag, Ingredient, Recipe

from users.serializers import UsersSerializer


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


class IngredientRecipeSerializer(ModelSerializer):
    """Сериализатор для Ingredient в Recipe"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


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


class RecipeListSerializer(ModelSerializer):
    """./"""

    tags = TagSerializer(many=True)
    author = UsersSerializer(many=False)
    ingredients = IngredientRecipeSerializer(many=True) #нет amount Как прокинуть? или написать другой сериализатор
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  # 'is_favorited',
                  # 'is_in_shopping_cart',
                  'name', 'text', 'cooking_time') # image добавить

    def create(self, validated_data):
        pass