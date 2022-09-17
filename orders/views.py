from rest_framework import generics

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderListView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ("status",)


class OrderDetailView(generics.ListCreateAPIView):
    # permission_classes = (IsOwnerOrReadOnly,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ("status",)
