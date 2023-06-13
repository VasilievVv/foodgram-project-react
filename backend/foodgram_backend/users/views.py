from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins

from .serializers import FollowSerializer

User = get_user_model()


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet
                    ):
    serializer_class = FollowSerializer
    search_fields = ('user__username', 'is_subscribed__username')

    def get_user(self):
        return self.request.user

    def get_queryset(self):
        return self.get_user().follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.get_user())
