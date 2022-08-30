# Generated by Django 4.1 on 2022-08-30 05:24

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("inventory", "0008_alter_stock_product_inventory"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("stale", "Stale"),
                            ("paid", "Paid"),
                            ("shipped", "Shipped"),
                            ("refunded", "Refunded"),
                        ],
                        default="created",
                        max_length=20,
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2, default=0.0, max_digits=10
                    ),
                ),
                (
                    "tax",
                    models.DecimalField(
                        decimal_places=2, default=0.0, max_digits=10
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2, default=0.0, max_digits=10
                    ),
                ),
                (
                    "paid",
                    models.DecimalField(
                        decimal_places=2, default=0.0, max_digits=10
                    ),
                ),
                ("shipping_address", models.TextField(blank=True, null=True)),
                ("inventory_updated", models.BooleanField(default=False)),
                (
                    "product_inventory",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inventory.productinventory",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]