# Generated by Django 4.2.7 on 2023-11-07 22:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="Demo",
            field=models.TextField(
                blank=True, null=True, verbose_name="دمو توضیحات محصول"
            ),
        ),
    ]