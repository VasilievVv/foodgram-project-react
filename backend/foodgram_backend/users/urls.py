from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowlistView, FollowCreateView, CustomUserViewSet

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('users/subscriptions/', FollowlistView.as_view()),
    path('users/<int:pk>/subscribe/', FollowCreateView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
