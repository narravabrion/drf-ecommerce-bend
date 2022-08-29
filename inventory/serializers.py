from rest_framework import serializers

from inventory.models import (
    Category,
    Media,
    Product,
    ProductInventory,
    ProductType,
    Stock,
)
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
            "is_active",
        )


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    product_inventory = serializers.StringRelatedField(many=True)  # type: ignore
    category = CategorySerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "slug",
            "name",
            "description",
            "is_active",
            "category",
            "product_inventory",
            "owner",
        )


class ProductInventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_type = ProductTypeSerializer(read_only=True)
    media = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Media.objects.all()
    )
    product_inventory_stock = serializers.PrimaryKeyRelatedField(  # type: ignore
        read_only=True
    )

    class Meta:
        model = ProductInventory
        fields = (
            "sku",
            "product_type",
            "product",
            "is_active",
            "is_default",
            "retail_price",
            "store_price",
            "sale_price",
            "is_on_sale",
            "weight",
            "media",
            "product_inventory_stock",
        )


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            "product_inventory",
            "image",
            "alt_text",
        )


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            "product_inventory",
            "last_checked",
            "units",
            "units_sold",
        )
