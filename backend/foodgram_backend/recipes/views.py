from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tag, Ingredient, Favorite, Recipe, ShoppingCart, RecipeIngredients
from .pagination import CustomPaginator
from .serializers import (TagSerializer, IngredientSerializer,
                          FavoriteSerializer, ShoppingCartSerializer,
                          RecipeListSerializer, RecipeCreateSerializer)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """/."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """/."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class FavoriteView(generics.CreateAPIView,
                   generics.DestroyAPIView):
    """./"""

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = FavoriteSerializer(recipe, data=request.data)
        if serializer.is_valid():
            if Favorite.objects.filter(user=request.user, recipe=recipe):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(recipe=recipe, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,  request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        get_object_or_404(Favorite, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(views.APIView):
    """./"""
    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def get(self, request):
        user = request.user
        recipes_in_cart = RecipeIngredients.objects.filter(
            recipe__cart_recipe__user=user)
        ingredients = recipes_in_cart.values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(
            ingredient_sum=Sum('amount')
        )
        shopping_list = 'Список покупок: \n'
        for ingredient in ingredients:
            shopping_list += (
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["ingredient_sum"]} '
                f'({ingredient["ingredient__measurement_unit"]})\n'
            )
            response = HttpResponse(
                shopping_list, content_type='text/plain; charset=utf8')
            response[
                'Content-Disposition'
            ] = f'attachment; filename=shopping_list.txt'
        return response



    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = ShoppingCartSerializer(recipe, data=request.data)
        if serializer.is_valid():
            ShoppingCart.objects.create(recipe=recipe, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        get_object_or_404(ShoppingCart, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeListCreateView(generics.ListCreateAPIView):
    """././"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateSerializer
        return RecipeListSerializer


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """././."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return RecipeCreateSerializer
        return RecipeListSerializer

