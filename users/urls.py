from django.urls import path

from users.views import UserListApiView

urlpatterns = [
    path("user/", UserListApiView.as_view(), name="user"),
    path(
        "user/<str:id>/detail/", UserListApiView.as_view(), name="user-detail"
    ),
]
