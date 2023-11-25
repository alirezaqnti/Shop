# Generated by Django 4.2.7 on 2023-11-25 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Users", "0002_remove_userinfo_email"),
        ("Main", "0003_remove_address_firstname_remove_address_lastname_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="User",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="Users.userinfo",
                verbose_name="",
            ),
            preserve_default=False,
        ),
    ]
