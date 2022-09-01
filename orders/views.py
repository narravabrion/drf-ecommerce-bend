from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from orders.models import Order
from orders.permissions import IsOwnerOrReadOnly
from orders.serializers import OrderSerializer


class OrderListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ("status",)


class OrderDetailView(generics.ListCreateAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ("status",)
