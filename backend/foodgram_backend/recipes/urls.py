from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import TagViewSet, IngredientViewSet


router_api_v1 = SimpleRouter()

router_api_v1.register('tags', TagViewSet)
router_api_v1.register('ingredients', IngredientViewSet)


urlpatterns = [

    path('', include(router_api_v1.urls)),
]