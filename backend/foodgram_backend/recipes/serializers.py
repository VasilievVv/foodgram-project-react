from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (Tag, Ingredient, Recipe,
                     RecipeIngredients, Favorite, ShoppingCart)
from .specialserializer import Hex2NameColor, Base64ImageField
from users.serializers import UsersSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для Тегов."""

    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для списка Ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для Ингредиентов в Рецепте."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для Избранного."""

    name = serializers.CharField(required=False)
    # image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для Списка покупок."""

    name = serializers.CharField(required=False)
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка Рецептов."""

    tags = TagSerializer(read_only=True, many=True)
    author = UsersSerializer(read_only=True, many=False)
    ingredients = IngredientRecipeSerializer(source='recipe_ingredients',
                                             read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time', )

    def get_is_favorited(self, value):
        user = self.context.get('request').user
        return (user.is_authenticated
                and Favorite.objects.filter(
                    user=user,
                    recipe=value.id).exists())

    def get_is_in_shopping_cart(self, value):
        user = self.context.get('request').user
        return (user.is_authenticated
                and ShoppingCart.objects.filter(
                    user=user,
                    recipe=value.id).exists())


class RecipeIngredientIdSerializer(serializers.ModelSerializer):
    """Дополнительный сериализатор Интредиентов при создании Рецепта."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания/обновления Рецепта."""

    id = serializers.ReadOnlyField()
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    author = UsersSerializer(read_only=True,
                             default=serializers.CurrentUserDefault())
    ingredients = RecipeIngredientIdSerializer(many=True, required=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time', )
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('author', 'name', ),
                message='Такой рецепт уже добавлен',
            )
        ]

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError('Добавьте ингредиент')
        return value

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

    def get_is_favorited(self, value):
        user = self.context.get('request').user
        return (user.is_authenticated
                and Favorite.objects.filter(
                    user=user,
                    recipe=value.id).exists())

    def get_is_in_shopping_cart(self, value):
        user = self.context.get('request').user
        return (user.is_authenticated
                and ShoppingCart.objects.filter(
                    user=user,
                    recipe=value.id).exists())
