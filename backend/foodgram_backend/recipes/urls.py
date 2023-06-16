from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import TagViewSet, IngredientViewSet, FavoreteView, ShoppingCartView


router_api_v1 = SimpleRouter()

router_api_v1.register('tags', TagViewSet)
router_api_v1.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('recipes/<int:pk>/favorite/', FavoreteView.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartView.as_view()),
    path('', include(router_api_v1.urls)),
]