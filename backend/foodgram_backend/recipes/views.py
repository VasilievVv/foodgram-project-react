from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, views, status, generics, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tag, Ingredient, Favorite, Recipe, ShoppingCart, RecipeIngredients
from .pagination import CustomPaginator
from .permissions import IsAuthorOrReadOnly
from .filter import RecipeFilter
from .serializers import (TagSerializer, IngredientSerializer,
                          FavoriteSerializer, ShoppingCartSerializer,
                          RecipeListSerializer, RecipeCreateSerializer)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для Тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для Ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class FavoriteView(generics.CreateAPIView,
                   generics.DestroyAPIView):
    """View class для Избранного."""

    permission_classes = [permissions.IsAuthenticated]

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
    """View class для Списка покупок."""

    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='download_shopping_cart',
            permission_classes=[permissions.IsAuthenticated])
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
    """View class для создания рецепта и вывода списка рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    pagination_class = CustomPaginator
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    filterset_fields = ('author', 'tags',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateSerializer
        return RecipeListSerializer

    def get_queryset(self):
        def _get_queryset_params(params):
            if self.request.query_params.get(params) == '1':
                return True
            return False

        user = self.request.user

        if _get_queryset_params('is_favorited'):
            return Recipe.objects.filter(favorite_recipe__user=user)

        if _get_queryset_params('is_in_shopping_cart'):
            return Recipe.objects.filter(cart_recipe__user=user)

        return Recipe.objects.all()


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View class для вывода информации о рецепте, его удаления и изменения."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return RecipeCreateSerializer
        return RecipeListSerializer
