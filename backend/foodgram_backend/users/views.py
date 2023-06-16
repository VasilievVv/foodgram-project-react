from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status, views
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowListSerializer

User = get_user_model()


class FollowlistView(views.APIView):

    def get(self, request):
        following = User.objects.filter(following__user=self.request.user)
        serializer = FollowListSerializer(following,
                                          many=True,
                                          context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowCreateView(views.APIView):
    """./"""

    def post(self, request, pk):
        following = get_object_or_404(User, id=pk)
        serializer = FollowListSerializer(following, data=request.data)
        if serializer.is_valid():
            Follow.objects.create(user=request.user, following=following)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        following = get_object_or_404(User, id=pk)
        Follow.objects.delete(users=request.user, following=following)
        return Response(status=status.HTTP_204_NO_CONTENT)
