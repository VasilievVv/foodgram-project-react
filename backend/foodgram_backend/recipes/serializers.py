from rest_framework import serializers

from .models import Tag, Ingredient, Recipe, RecipeIngredients, Favorite, ShoppingCart

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

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для Избранного."""

    name = serializers.CharField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time') # 'image' добавить


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для Списка покупок."""

    name = serializers.CharField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time') # 'image' добавить


class RecipeListSerializer(serializers.ModelSerializer):
    """./"""

    tags = TagSerializer(read_only=True, many=True)
    author = UsersSerializer(read_only=True, many=False)
    ingredients = IngredientRecipeSerializer(source='recipe_ingredients',
                                             read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name', 'text', 'cooking_time') # image добавить

    def get_is_favorited(self, value):
        user = self.context.get('request').user
        return Favorite.objects.filter(user=user, recipe=value.id).exists()

    def get_is_in_shopping_cart(self, value):
        user = self.context.get('request').user
        return ShoppingCart.objects.filter(user=user, recipe=value.id).exists()


class RecipeIngredientIdSerializer(serializers.ModelSerializer):
    """;;';"""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """//"""

    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = RecipeIngredientIdSerializer(many=True,)

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
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=value.get('id'),
                amount=value.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        pass

