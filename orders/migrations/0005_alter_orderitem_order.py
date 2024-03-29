# Generated by Django 4.1 on 2022-09-13 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_rename_price_orderitem_total_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="order_items",
                to="orders.order",
            ),
        ),
    ]
