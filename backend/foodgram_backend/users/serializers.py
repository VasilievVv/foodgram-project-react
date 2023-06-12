from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth import get_user_model


User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор User на ендпоинте - /api/users/
    при GET запросе вернет список пользователей
    при POST запросе"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            # 'is_subscribed', Добавить после
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
        )


# class SetPasswordSerializer(serializers.Serializer):
#     """Сериализатор смены пароля на ендпоинте -
#     POST /api/users/set-password/."""


# class FollowSerializer(serializers.ModelSerializer):
#     """"Сериализатор выаода инфы о подписке"""
#
#     user = serializers.SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#         default=serializers.CurrentUserDefault())
#     following = SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all())
#
#     class Meta:
#         fields = ('user', 'following')
#         model = Follow
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=['user', 'following']
#             )
#         ]
#
#     def validate(self, data):
#         """Проверяем, что не подписываемся на самого себя."""
#         if self.context['request'].user != data.get('following'):
#             return data
#         raise serializers.ValidationError("Нельзя подписаться на самого себя")