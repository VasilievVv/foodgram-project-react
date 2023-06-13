from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


User = get_user_model()










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
