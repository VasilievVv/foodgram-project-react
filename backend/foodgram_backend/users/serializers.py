from rest_framework import serializers

from django.contrib.auth import get_user_model

from recipes.models import Recipe
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
        requests = self.context.get('request')
        if requests.user.is_authenticated:
            return Follow.objects.filter(user=requests.user,
                                         following=obj).exists()
        return False


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для подписок."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', ) #image добавить


class FollowSerializer(serializers.ModelSerializer):
    """"Сериализатор вывода инфы о подписке и создания подкиски."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = FollowRecipeSerializer(read_only=True, many=True)
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

    def get_is_subscribed(self, value):
        return True

    def get_recipes_count(self, value):
        request = self.context.get('request')
        author = request.user
        return author.recipes.count()
