from rest_framework import viewsets
from rest_framework.response import Response

from .models import Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """/."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """/."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
