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


class MediaSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Media
        fields = (
            "image",
            "alt_text",
        )


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            "last_checked",
            "units",
            "units_sold",
        )


class ProductInventorySerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(  # type: ignore[var-annotated]
        read_only=True, view_name="product-detail", lookup_field="slug"
    )
    product_type = ProductTypeSerializer(read_only=True)
    media = MediaSerializer(many=True)
    product_inventory_stock = StockSerializer()

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


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    product_inventory = serializers.HyperlinkedRelatedField(  # type: ignore[var-annotated]
        read_only=True,
        many=True,
        view_name="product-inventory-detail",
        lookup_field="sku",
    )
    # product_inventory = serializers.StringRelatedField(many=True)  # type: ignore
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
