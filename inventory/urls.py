from django.urls import path

from inventory.views import (
    CategoryListApiView,
    MediaDetailAPiView,
    MediaListApiView,
    ProductDetailApiView,
    ProductInventoryDetailApiView,
    ProductInventoryListApiView,
    ProductListApiView,
    ProductTypeListApiView,
    StockDetailApiView,
    StockListApiView,
)

urlpatterns = [
    path(
        "inventory/categories/", CategoryListApiView.as_view(), name="category"
    ),
    path(
        "inventory/product-types/",
        ProductTypeListApiView.as_view(),
        name="product-types",
    ),
    path("inventory/products/", ProductListApiView.as_view(), name="product"),
    path(
        "inventory/product/<slug:slug>/detail/",
        ProductDetailApiView.as_view(),
        name="product-detail",
    ),
    path(
        "inventory/product-inventory/",
        ProductInventoryListApiView.as_view(),
        name="product-inventory",
    ),
    path(
        "inventory/product-inventory/<str:sku>/detail/",
        ProductInventoryDetailApiView.as_view(),
        name="product-inventory-detail",
    ),
    path("inventory/stock/", StockListApiView.as_view(), name="stock"),
    path(
        "inventory/stock/<str:pk>/detail/",
        StockDetailApiView.as_view(),
        name="stock",
    ),
    path("media/images/", MediaListApiView.as_view(), name="stock"),
    path(
        "media/images/<str:pk>/detail/",
        MediaDetailAPiView.as_view(),
        name="stock",
    ),
]
