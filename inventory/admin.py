from django.contrib import admin

from inventory.models import (
    Category,
    Media,
    Product,
    ProductInventory,
    ProductType,
    Stock,
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProductInventory)
admin.site.register(Media)
admin.site.register(Stock)
