# from django.db.models import Sum
from typing import Any

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
    product_inventory = serializers.HyperlinkedRelatedField(
        view_name="product-inventory-detail",
        queryset=ProductInventory.objects.all(),
        lookup_field="sku",
        # required=False,
    )

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
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "order_items",
            "status",
            "subtotal",
            "tax",
            "total",
            "paid",
            "shipping_address",
            "inventory_updated",
        )

    # create an order after calculating total price and taxes
    def create(self, validated_data: Any) -> Any:
        print(1)
        order_items_data = validated_data.pop("product_inventory")
        order = Order.objects.create(
            **validated_data, user=self.context.get("request").user  # type: ignore[union-attr]
        )
        for item in order_items_data:
            sku = item.get("sku")
            quantity = item.get("quantity")
            product_inventory = ProductInventory.objects.get(sku=sku)
            # total_price = (
            #     product_inventory.sale_price * quantity
            #     if product_inventory.is_on_sale
            #     else product_inventory.retail_price * quantity
            # )
            OrderItem.objects.create(
                order=order,
                product_inventory=product_inventory,
                # total_price=total_price,
                quantity=quantity,
            )
        # calculate total price and taxes
        # order.subtotal = order.order_items.aggregate(Sum("total_price"))[
        #     "total_price__sum"
        # ]
        # order.tax = order.subtotal * 0.08
        # order.total = order.subtotal + order.tax
        # order.save()
        return order
