import base64

from rest_framework import serializers
from django.core.files.base import ContentFile


from .models import Tag, Ingredient, Recipe, RecipeIngredients, Favorite, ShoppingCart

from users.serializers import UsersSerializer


class Base64ImageField(serializers.ImageField):
    """Сериализатор для изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
        return super().to_internal_value(data)

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
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для Списка покупок."""

    name = serializers.CharField(required=False)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )


class RecipeListSerializer(serializers.ModelSerializer):
    """./"""

    tags = TagSerializer(read_only=True, many=True)
    author = UsersSerializer(read_only=True, many=False)
    ingredients = IngredientRecipeSerializer(source='recipe_ingredients',
                                             read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time', )

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
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags',
                  'name', 'image', 'text', 'cooking_time', )

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
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)
        if 'ingredients' in validated_data:
            ingredients_value = validated_data.pop('ingredients')
            instance.recipe_ingredients.all().delete()

            for value in ingredients_value:
                RecipeIngredients.objects.create(
                    recipe=instance,
                    ingredient=value.get('id'),
                    amount=value.get('amount')
                )
        instance.save()
        return instance
