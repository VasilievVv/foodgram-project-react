from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet

router_api_v1 = DefaultRouter()
router_api_v1.register('users', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router_api_v1.urls)),
    # path('users/subscriptions/', FollowlistView.as_view()),
    # path('users/<int:pk>/subscribe/', FollowCreateView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
