from django.urls import path

from orders.views import OrderDetailView, OrderListView

urlpatterns = [
    path("order/", OrderListView.as_view(), name="order"),
    path(
        "order/<str:pk>/detail/",
        OrderDetailView.as_view(),
        name="order-detail",
    ),
]
