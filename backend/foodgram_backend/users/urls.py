from django.urls import include, path

from .views import FollowlistView, FollowCreateView

urlpatterns = [
    path('users/subscriptions/', FollowlistView.as_view()),
    path('users/<int:pk>/subscribe/', FollowCreateView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
