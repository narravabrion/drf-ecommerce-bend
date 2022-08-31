from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from inventory.models import ProductInventory
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
        Order, null=True, on_delete=models.SET_NULL, related_name="order_item"
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
