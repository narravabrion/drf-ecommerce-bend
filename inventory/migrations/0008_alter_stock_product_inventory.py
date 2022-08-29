# Generated by Django 4.1 on 2022-08-29 03:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0007_alter_productinventory_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="product_inventory",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="product_inventory_stock",
                to="inventory.productinventory",
            ),
        ),
    ]
