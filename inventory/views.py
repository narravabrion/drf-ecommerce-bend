from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from inventory.models import (
    Category,
    Media,
    Product,
    ProductInventory,
    ProductType,
    Stock,
)
from inventory.permissions import IsOwnerOrReadOnly
from inventory.serializers import (
    CategorySerializer,
    MediaSerializer,
    ProductInventorySerializer,
    ProductSerializer,
    ProductTypeSerializer,
    StockSerializer,
)


class CategoryListApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductTypeListApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()


class ProductListApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "slug"


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "slug"


class ProductInventoryListApiView(generics.ListCreateAPIView):
    serializer_class = ProductInventorySerializer
    queryset = ProductInventory.objects.all()


class ProductInventoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductInventorySerializer
    queryset = ProductInventory.objects.all()
    lookup_field = "sku"


class StockListApiView(generics.ListAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class StockDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class MediaListApiView(generics.ListCreateAPIView):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()


class MediaDetailAPiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()
