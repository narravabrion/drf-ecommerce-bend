# Generated by Django 4.1 on 2022-08-30 12:13

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0008_alter_stock_product_inventory"),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="product_inventory",
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=0)),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="orders.order",
                    ),
                ),
                (
                    "product_inventory",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inventory.productinventory",
                    ),
                ),
            ],
        ),
    ]
