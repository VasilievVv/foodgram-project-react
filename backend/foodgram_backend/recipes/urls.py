from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (TagViewSet, IngredientViewSet, FavoriteView,
                    ShoppingCartView, RecipeListCreateView, RecipeDetailView)

router_api_v1 = SimpleRouter()

router_api_v1.register('tags', TagViewSet)
router_api_v1.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view()),
    path('recipes/<int:pk>/', RecipeDetailView.as_view()),
    path('recipes/<int:pk>/favorite/', FavoriteView.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartView.as_view()),
    path('recipes/download_shopping_cart/', ShoppingCartView.as_view()),
    path('', include(router_api_v1.urls)),
]
