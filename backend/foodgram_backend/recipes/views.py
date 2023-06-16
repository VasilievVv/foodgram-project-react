from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views, status
from rest_framework.response import Response

from .models import Tag, Ingredient, Favorite, Recipe
from .serializers import TagSerializer, IngredientSerializer, FavoriteSerializer

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """/."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """/."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class FavoreteView(views.APIView):
    """./"""

    def post(self, request, pk):
        # такая реализация дает возможность создавать одинаковые записи, нужна валидация
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = FavoriteSerializer(recipe, data=request.data)
        if serializer.is_valid():
            Favorite.objects.create(recipe=recipe, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,  request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        get_object_or_404(Favorite, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)