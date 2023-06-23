from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response

from djoser.views import UserViewSet

from recipes.pagination import CustomPaginator
from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Добавляем пагинацию."""

    pagination_class = CustomPaginator


class FollowlistView(generics.ListAPIView):
    """./"""

    pagination_class = CustomPaginator

    def get(self, request):
        following = User.objects.filter(
            following__user=self.request.user).order_by('id')
        paginate_queryset = self.paginate_queryset(following)
        serializer = FollowSerializer(
            paginate_queryset,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)


class FollowCreateView(generics.CreateAPIView,
                       generics.DestroyAPIView):
    """./"""

    def post(self, request, pk):
        following = get_object_or_404(User, id=pk)
        serializer = FollowSerializer(
            following,
            data=request.data,
            context={'request': request})
        if serializer.is_valid():
            Follow.objects.create(user=request.user, following=following)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        following = get_object_or_404(User, id=pk)
        get_object_or_404(Follow, user=request.user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
