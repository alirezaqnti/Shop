# Generated by Django 4.2.7 on 2023-11-10 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Products", "0004_alter_guarantee_options_remove_filters_type_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductFilter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Filter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fil_fil",
                        to="Products.filtervalue",
                        verbose_name="فیلتر",
                    ),
                ),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fil_prd",
                        to="Products.product",
                        verbose_name="محصول",
                    ),
                ),
            ],
            options={
                "verbose_name": "productfilter",
                "verbose_name_plural": "productfilters",
            },
        ),
    ]
