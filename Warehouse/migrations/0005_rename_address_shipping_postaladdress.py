# Generated by Django 4.2.7 on 2023-11-25 17:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Warehouse", "0004_alter_cart_amount_alter_cart_totaldiscount_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="shipping",
            old_name="Address",
            new_name="PostalAddress",
        ),
    ]
