from decimal import Decimal
from typing import Any
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from inventory.models import ProductInventory, Stock
from users.abstracts import TimeStampedModel

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("stale", "Stale"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
)


class Order(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        null=False,
        blank=False,
        default=uuid4,
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="created"
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.TextField(blank=True, null=True)
    inventory_updated = models.BooleanField(default=False)


class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        null=False,
        blank=False,
        default=uuid4,
    )
    order = models.ForeignKey(
        Order, null=True, on_delete=models.CASCADE, related_name="order_items"
    )
    product_inventory = models.ForeignKey(
        ProductInventory,
        null=True,
        on_delete=models.SET_NULL,
        related_name="product_inventory",
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    quantity = models.PositiveIntegerField(default=0, null=False, blank=False)


# calculate total price and taxes for an order
def calculate_order_total(order: Order) -> None:
    if order is not None and order.order_items.count() > 0:
        order_items = order.order_items.all()
        order_total = order_items.aggregate(Sum("total_price"))[
            "total_price__sum"
        ]
        order_tax = order_total * Decimal(0.08)
        order_total = order_total + order_tax
        order.subtotal = order_total - order_tax
        order.tax = order_tax
        order.total = order_total
        order.save()


# update inventory after an order is created
def update_inventory(order: Order) -> None:
    if order is not None and order.order_items.count() > 0:
        for order_item in order.order_items.all():
            if order_item.product_inventory is not None:
                stock = Stock.objects.get(
                    product_inventory=order_item.product_inventory
                )
                stock.units -= order_item.quantity
                stock.units_sold += order_item.quantity
                stock.save()
                order_item.product_inventory.save()
        order.inventory_updated = True
        order.save()


def calculate_order_item_total(order_item: OrderItem) -> None:
    order_item.total_price = (
        order_item.product_inventory.sale_price * order_item.quantity  # type: ignore
        if order_item.product_inventory.is_on_sale  # type: ignore
        else order_item.product_inventory.retail_price * order_item.quantity  # type: ignore
    )
    order_item.save()


# update order everytime an order item is saved
@receiver(pre_save, sender=OrderItem)
def update_order_item(sende: Any, instance: Any, **kwargs: Any) -> None:
    instance.total_price = (
        instance.product_inventory.sale_price * instance.quantity
        if instance.product_inventory.is_on_sale
        else instance.product_inventory.retail_price * instance.quantity
    )
    order = instance.order
    calculate_order_total(order)
    update_inventory(order)


# update order everytime an order item is deleted
@receiver(pre_delete, sender=OrderItem)
def update_order_item_delete(
    sender: Any, instance: Any, **kwargs: Any
) -> None:
    order = instance.order
    if order:
        calculate_order_total(order)
        order.inventory_updated = True
        stock = Stock.objects.get(product_inventory=instance.product_inventory)
        stock.units += instance.quantity
        stock.units_sold -= instance.quantity
        order.save()
        stock.save()
        instance.product_inventory.save()
