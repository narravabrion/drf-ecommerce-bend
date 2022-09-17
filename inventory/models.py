from typing import Any
from uuid import uuid4

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from users.abstracts import TimeStampedModel

User = get_user_model()


class Category(models.Model):

    CATEGORIES = (
        ("decorative", "decorative"),
        ("commercial", "commercial"),
        ("fine_art", "fine art"),
    )

    name = models.CharField(max_length=100, choices=CATEGORIES)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    is_active = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")

    def __str__(self) -> str:
        return self.name


@receiver(pre_save, sender=Category)
def slug_pre_save_category(sender: Any, instance: Any, **kwargs: Any) -> None:
    instance.slug = slugify(instance.name)


class ProductType(models.Model):
    TYPES = (
        ("painting", "painting"),
        ("sculpture", "sculpture"),
        ("DIY", "DIY"),
        ("beadwork", "beadwork"),
        ("photography", "photography"),
        ("drawing", "drawing"),
        ("claywork", "claywork"),
    )
    name = models.CharField(max_length=255, unique=True, choices=TYPES)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def __str__(self) -> str:
        return self.name


@receiver(pre_save, sender=ProductType)
def slug_pre_save_product_type(
    sender: Any, instance: Any, **kwargs: Any
) -> None:
    instance.slug = slugify(instance.name)


class Product(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid4, unique=True, editable=False, name="id"
    )
    owner = models.ForeignKey(
        User,
        related_name="owner",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    slug = models.SlugField(max_length=255, blank=True)
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        related_name="product_category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self) -> str:
        return self.name


@receiver(pre_save, sender=Product)
def slug_pre_save_product(sender: Any, instance: Any, **kwargs: Any) -> None:
    if instance.slug is None or instance.slug == "":
        slug_string = f"{instance.name}-{instance.id}"
        instance.slug = slugify(slug_string[0:250])


class ProductInventory(TimeStampedModel):
    sku = models.CharField(
        max_length=20,
        unique=True,
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="product_type",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product, related_name="product_inventory", on_delete=models.PROTECT
    )
    is_active = models.BooleanField(
        default=False,
    )
    is_default = models.BooleanField(
        default=False,
    )

    retail_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        error_messages={
            "name": {
                "max_length": _(
                    "the price must be between 0 and 99999999.99."
                ),
            },
        },
    )
    store_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        error_messages={
            "name": {
                "max_length": _(
                    "the price must be between 0 and 99999999.99."
                ),
            },
        },
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        error_messages={
            "name": {
                "max_length": _(
                    "the price must be between 0 and 99999999.99."
                ),
            },
        },
    )
    is_on_sale = models.BooleanField(
        default=False,
    )
    weight = models.FloatField()

    class Meta:
        verbose_name_plural = _("product inventories")

    def __str__(self) -> str:
        return self.sku


class Media(TimeStampedModel):
    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.CASCADE,
        related_name="media",
    )
    image = CloudinaryField("image")
    alt_text = models.CharField(
        max_length=255,
    )

    class Meta:
        verbose_name_plural = "media"

    def __str__(self) -> str:
        return self.alt_text


class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name="product_inventory_stock",
        on_delete=models.CASCADE,
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
    )
    units = models.PositiveIntegerField(
        default=0,
    )
    units_sold = models.IntegerField(
        default=0,
    )
