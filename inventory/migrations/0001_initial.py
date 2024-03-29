# Generated by Django 4.1 on 2022-08-26 14:53

import uuid

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("DECORATIVE", "decorative"),
                            ("COMMERCIAL", "commercial"),
                            ("FINE_ART", "fine art"),
                        ],
                        max_length=100,
                    ),
                ),
                ("slug", models.SlugField(max_length=150, unique=True)),
                ("is_active", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                        unique=True,
                    ),
                ),
                ("slug", models.SlugField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_category",
                        to="inventory.category",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductInventory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sku", models.CharField(max_length=20, unique=True)),
                ("is_active", models.BooleanField(default=False)),
                ("is_default", models.BooleanField(default=False)),
                (
                    "retail_price",
                    models.DecimalField(
                        decimal_places=2,
                        error_messages={
                            "name": {
                                "max_length": "the price must be between 0 and 99999999.99."
                            }
                        },
                        max_digits=10,
                    ),
                ),
                (
                    "store_price",
                    models.DecimalField(
                        decimal_places=2,
                        error_messages={
                            "name": {
                                "max_length": "the price must be between 0 and 99999999.99."
                            }
                        },
                        max_digits=10,
                    ),
                ),
                (
                    "sale_price",
                    models.DecimalField(
                        decimal_places=2,
                        error_messages={
                            "name": {
                                "max_length": "the price must be between 0 and 99999999.99."
                            }
                        },
                        max_digits=10,
                    ),
                ),
                ("is_on_sale", models.BooleanField(default=False)),
                ("weight", models.FloatField()),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="product",
                        to="inventory.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("PAINTING", "painting"),
                            ("SCULPTURE", "sculpture"),
                            ("DIY", "DIY"),
                            ("BEADROCK", "beadwork"),
                            ("PHOTOGRAPHY", "photography"),
                            ("DRAWING", "drawing"),
                            ("CLAYWORK", "claywork"),
                        ],
                        max_length=255,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("last_checked", models.DateTimeField(blank=True, null=True)),
                ("units", models.IntegerField(default=0)),
                ("units_sold", models.IntegerField(default=0)),
                (
                    "product_inventory",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="product_inventory",
                        to="inventory.productinventory",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="productinventory",
            name="product_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="product_type",
                to="inventory.producttype",
            ),
        ),
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        max_length=255, verbose_name="image"
                    ),
                ),
                ("alt_text", models.CharField(max_length=255)),
                (
                    "product_inventory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="media",
                        to="inventory.productinventory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
