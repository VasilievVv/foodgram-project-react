from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views
from .views import UsersViewSet, UserDetailView

router_api_v1 = SimpleRouter()


router_api_v1.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path('users/me/', views.UsersMeView.as_view(), ),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('', include(router_api_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
