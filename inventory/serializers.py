from typing import Any

from rest_framework import serializers

from inventory.models import (
    Category,
    Media,
    Product,
    ProductInventory,
    ProductType,
    Stock,
)


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
        queryset=Product.objects.all(),
        view_name="product-detail",
        lookup_field="slug",
    )
    product_type = serializers.SlugRelatedField(
        queryset=ProductType.objects.all(), slug_field="name"
    )
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

    # enable saving of nested fields in a single save
    def create(self, validated_data: dict) -> ProductInventory:
        media_data = validated_data.pop("media")
        stock_data = validated_data.pop("product_inventory_stock")
        product_inventory = ProductInventory.objects.create(**validated_data)
        for media in media_data:
            Media.objects.create(product_inventory=product_inventory, **media)
        Stock.objects.create(product_inventory=product_inventory, **stock_data)
        return product_inventory

    def update(
        self, instance: ProductInventory, validated_data: dict
    ) -> ProductInventory:
        media_data = validated_data.pop("media")
        stock_data = validated_data.pop("product_inventory_stock")
        instance.__dict__.update(**validated_data)
        instance.save()
        for media in media_data:
            media_instance, created = Media.objects.get_or_create(
                **media, product_inventory=instance
            )
            if not created:
                media_instance.__dict__.update(**media)
                media_instance.save()
        stock_instance, created = Stock.objects.get_or_create(
            defaults=stock_data, product_inventory=instance
        )
        if not created:
            stock_instance.__dict__.update(**stock_data)
            stock_instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    product_inventory = serializers.HyperlinkedRelatedField(  # type: ignore[var-annotated]
        read_only=True,
        many=True,
        view_name="product-inventory-detail",
        lookup_field="sku",
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="name"
    )
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)  # type: ignore[var-annotated]

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

    def create(self, validated_data: Any) -> Any:
        product = Product.objects.create(
            **validated_data, owner=self.context.get("request").user  # type: ignore[union-attr]
        )
        return product
