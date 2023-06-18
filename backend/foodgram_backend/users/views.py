from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status,viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """>./"""

    @action(methods=['get'],
            detail=False, )
    def subscriptions(self, request):
        """...0"""

        following = User.objects.filter(following__user=self.request.user)
        serializer = FollowSerializer(following, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk):
        """../"""

        following = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            serializer = FollowSerializer(following, data=request.data, context={'request': request})
            if serializer.is_valid():
                Follow.objects.create(user=request.user, following=following)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        get_object_or_404(Follow, user=request.user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


