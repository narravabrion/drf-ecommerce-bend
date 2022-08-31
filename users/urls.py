from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import UserCreateApiView, UserListApiView

urlpatterns = [
    path("user/", UserListApiView.as_view(), name="user"),
    path("user/register/", UserCreateApiView.as_view(), name="register"),
    path(
        "user/<str:id>/detail/", UserListApiView.as_view(), name="user-detail"
    ),
    path(
        "auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
]
