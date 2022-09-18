from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    UserCreateApiView,
    UserDetailView,
    UserListApiView,
    UserTokenObtainPairView,
)

urlpatterns = [
    path("user/", UserListApiView.as_view(), name="user"),
    path("user/register/", UserCreateApiView.as_view(), name="register"),
    path(
        "user/<str:id>/detail/", UserDetailView.as_view(), name="user-detail"
    ),
    path(
        "auth/login/",
        UserTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
]
