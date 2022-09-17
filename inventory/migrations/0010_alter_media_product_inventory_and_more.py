# Generated by Django 4.1 on 2022-09-12 09:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0009_alter_category_name_alter_producttype_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="media",
            name="product_inventory",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="media",
                to="inventory.productinventory",
            ),
        ),
        migrations.AlterField(
            model_name="stock",
            name="product_inventory",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_inventory_stock",
                to="inventory.productinventory",
            ),
        ),
    ]
