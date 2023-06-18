from rest_framework import serializers

from .models import Tag, Ingredient, Recipe

from users.serializers import UsersSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для Tag."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для Ingredient."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для Ingredient в Recipe"""
    name = serializers.CharField(required=False)
    measurement_unit = serializers.CharField(required=False)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для Избранного."""

    name = serializers.CharField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time') # 'image' добавить


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для Списка покупок."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time') # 'image' добавить


class RecipeListSerializer(serializers.ModelSerializer):
    """./"""

    tags = TagSerializer(read_only=True, many=True)
    author = UsersSerializer(read_only=True,many=False)
    ingredients = IngredientRecipeSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  # 'is_favorited',
                  # 'is_in_shopping_cart',
                  'name', 'text', 'cooking_time') # image добавить


class RecipeCreateSerializer(serializers.ModelSerializer):
    """//"""

    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = IngredientRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags',

                  'name', 'text', 'cooking_time') # image добавить

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        author = self.context['request'].user
        ingredients_value = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.set(tags)
        for value in ingredients_value:
            id, amount = recipe.ingredients.get_or_create(**value)
            # RecipeIngredients.objects.create(id=id, amount=amount)
            # recipe.ingredients.add(ingredient=value['id'],
            #                        amount=value['amount'])
        return recipe

