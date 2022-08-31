from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer, UserTokenObtainPairSerializer

User = get_user_model()


class UserListApiView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserTokenObtainPairView(TokenObtainPairView):  # type: ignore[no-any-unimported]
    serializer_class = UserTokenObtainPairSerializer
