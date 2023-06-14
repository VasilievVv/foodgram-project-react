from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet
                    ):
    """./"""

    queryset = Follow.objects.all()
    # def get_user(self):
    #     return self.request.user
    #
    # def get_queryset(self):
    #     return self.get_user().follower.all()

    @action(methods=['get'],
            detail=False, )
    def subscriptions(self, request):
        """../"""

        queryset = self.request.user.follower.all()
        serializer = FollowSerializer(queryset, many=True,)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'DELETE'], detail=True)
    def subscribe(self, request, pk):
        """../"""

        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            serializer = FollowSerializer(author, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            pass


    # serializer_class = FollowSerializer
    # search_fields = ('user__username', 'is_subscribed__username')


    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.get_user())
