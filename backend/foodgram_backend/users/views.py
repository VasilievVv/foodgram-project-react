from django.contrib.auth import get_user_model

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UsersSerializer, UsersMeSerializer

User = get_user_model()


class UsersViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet
                   ):
    """
    Получение списка всех пользователей, добавление нового пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UsersSerializer


class UsersMeView(APIView):
    """
    Любой пользователь может получить информацию о себе.
    """

    def get(self, request):
        user = self.request.user
        serializer = UsersMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    Получаем информацию о пользователе.
    """

    def get(self, request, pk):
        """Получаем инфу по id."""

        user = User.objects.get(id=pk,)
        serializer = UsersMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class FollowViewSet(mixins.CreateModelMixin,
#                     mixins.ListModelMixin,
#                     viewsets.GenericViewSet
#                     ):
#     serializer_class = FollowSerializer
#     search_fields = ('user__username', 'following__username')
#
#     def get_user(self):
#         return self.request.user
#
#     def get_queryset(self):
#         return self.get_user().follower.all()
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.get_user())
