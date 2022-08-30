from rest_framework import serializers

from inventory.models import ProductInventory
from orders.models import Order, OrderItem


class OrderProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = (
            "sku",
            "retail_price",
            "store_price",
            "sale_price",
            "is_on_sale",
        )


class OrderItemSerializer(serializers.ModelSerializer):
    product_inventory = OrderProductInventorySerializer()

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "total_price",
            "quantity",
            "order",
            "product_inventory",
        )


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "order_item",
            "status",
            "subtotal",
            "tax",
            "total",
            "paid",
            "shipping_address",
            "inventory_updated",
        )
