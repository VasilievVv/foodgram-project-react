from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

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

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)

    def get_is_subscribed(self, obj):
        requests = self.context.get('request')
        if requests.user.is_authenticated:
            return Follow.objects.filter(user=requests.user,
                                         following=obj).exists()
        return False


class FollowSerializer(serializers.ModelSerializer):
    """"Сериализатор выаода инфы о подписке."""

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
            # 'recipes',
            # 'recipes_count', пока хз
        )
    # user = serializers.SlugRelatedField(
    #     slug_field='username',
    #     read_only=True,
    #     default=serializers.CurrentUserDefault())
    # is_subscribed = SlugRelatedField(
    #     slug_field='username',
    #     queryset=User.objects.all())

    def get_is_subscribed(self, obj):
        requests = self.context.get('request')
        if requests.user.is_authenticated:
            return Follow.objects.filter(user=requests.user,
                                         following=obj).exists()
        return False
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=['user', 'is_subscribed']
        #     )
        # ]

    # def validate(self, data):
    #     """Проверяем, что не подписываемся на самого себя."""
    #     if self.context['request'].user != data.get('is_subscribed'):
    #         return data
    #     raise serializers.ValidationError("Нельзя подписаться на самого себя")