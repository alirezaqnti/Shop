# Generated by Django 4.2.7 on 2023-11-13 19:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Warehouse", "0002_alter_cartproduct_amount_alter_cartproduct_fee"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="Tax",
        ),
        migrations.RemoveField(
            model_name="cartproduct",
            name="Tax",
        ),
    ]
