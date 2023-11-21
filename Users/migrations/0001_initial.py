# Generated by Django 4.2.7 on 2023-11-04 19:20

import Users.models
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserInfo",
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
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                (
                    "Email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="ایمیل"
                    ),
                ),
                (
                    "Phone",
                    models.CharField(
                        max_length=13, unique=True, verbose_name="شماره تماس"
                    ),
                ),
                ("Password", models.CharField(max_length=250, verbose_name="رمز عبور")),
                ("key", models.BinaryField(blank=True, max_length=200, null=True)),
                ("Name", models.CharField(max_length=100, verbose_name="نام")),
                (
                    "Iban",
                    models.CharField(
                        blank=True, max_length=26, null=True, verbose_name="شماره شبا"
                    ),
                ),
                (
                    "Gender",
                    models.IntegerField(
                        choices=[(1, "Male"), (2, "Female")],
                        default=2,
                        verbose_name="جنسیت",
                    ),
                ),
                (
                    "CreaditCard",
                    models.CharField(
                        blank=True, max_length=16, null=True, verbose_name="شماره کارت"
                    ),
                ),
                (
                    "ProfileImage",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=Users.models.UsersProfile,
                        verbose_name="تصویر پروفایل",
                    ),
                ),
                (
                    "Phone_Confirm",
                    models.BooleanField(default=False, verbose_name="تاییدیه موبایل"),
                ),
                (
                    "Email_Confirm",
                    models.BooleanField(default=False, verbose_name="تاییدیه ایمیل"),
                ),
                (
                    "Joined_At",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت"),
                ),
                (
                    "Joined_At_J",
                    models.CharField(
                        default=Users.models.JDATE,
                        editable=False,
                        max_length=100,
                        verbose_name="تاریخ عضویت",
                    ),
                ),
                (
                    "Left_At",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاریخ قطع همکاری"
                    ),
                ),
                (
                    "Modified_At",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ اخرین تغییر"
                    ),
                ),
                (
                    "Modified_At_J",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="تاریخ اخرین تغییر",
                    ),
                ),
                (
                    "Last_Login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="اخرین ورود"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "کاربران",
            },
        ),
        migrations.CreateModel(
            name="Userlogs",
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
                    "Data",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True, verbose_name="دیتا"
                    ),
                ),
                (
                    "Created_At",
                    models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت"),
                ),
                (
                    "Created_At_J",
                    models.CharField(
                        default=Users.models.JDATE,
                        editable=False,
                        max_length=100,
                        verbose_name="تاریخ عضویت",
                    ),
                ),
                (
                    "Parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Users.userinfo",
                        verbose_name="والد",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Userlogs",
            },
        ),
    ]
