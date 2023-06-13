from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор User на ендпоинте - /api/users/
    при GET запросе вернет список пользователей
    при POST запросе"""

    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UsersMeSerializer(serializers.ModelSerializer):
    """Сериализатор вывода информации о текущем пользователе
    на ендпоитне - GET /api/users/me/"""

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


class FollowSerializer(serializers.ModelSerializer):
    """"Сериализатор выаода инфы о подписке"""

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    is_subscribed = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        fields = ('user', 'is_subscribed')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'is_subscribed']
            )
        ]

    def validate(self, data):
        """Проверяем, что не подписываемся на самого себя."""
        if self.context['request'].user != data.get('is_subscribed'):
            return data
        raise serializers.ValidationError("Нельзя подписаться на самого себя")