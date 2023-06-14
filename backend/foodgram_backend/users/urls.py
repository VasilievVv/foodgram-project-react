from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet

router_api_v1 = DefaultRouter()
router_api_v1.register('follow', FollowViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include(router_api_v1.urls)),

]
