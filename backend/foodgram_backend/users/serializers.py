from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe
from recipes.specialserializer import Base64ImageField
from .models import Follow

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор User на ендпоинте - /api/users/
    при GET запросе вернет список пользователей
   """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and Follow.objects.filter(
                    user=user,
                    following=obj).exists())


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для подписок."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )


class FollowSerializer(serializers.ModelSerializer):
    """"Сериализатор вывода инфы о подписке и создания подкиски."""

    is_subscribed = serializers.SerializerMethodField()
    # recipes = FollowRecipeSerializer(read_only=True, many=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField()
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def validate(self, value):
        """Проверяем, что не подписываемся на самого себя."""

        request = self.context.get('request')
        author = request.user
        if author != value:
            return value
        raise serializers.ValidationError("Нельзя подписаться на самого себя")

    def get_recipes(self, value):
        recipes_limit = int(self.context.get('recipes_limit'))
        request = self.context.get('request')
        author = request.user
        if recipes_limit:
            recipes = Recipe.objects.filter(author=author)[:recipes_limit]
        else:
            recipes = Recipe.objects.filter(author=author).all()
        serializer = FollowRecipeSerializer(recipes, many=True,
                                            context=self.context)
        return serializer.data

    def get_is_subscribed(self, value):
        return True

    def get_recipes_count(self, value):
        request = self.context.get('request')
        author = request.user
        return author.recipes.count()
