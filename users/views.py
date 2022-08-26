from django.contrib.auth import get_user_model
from rest_framework import generics

from users.serializers import UserSerializer

User = get_user_model()


class UserListApiView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
