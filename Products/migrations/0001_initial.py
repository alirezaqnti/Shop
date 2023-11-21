# Generated by Django 4.2.7 on 2023-11-04 19:20

import Products.models
import ckeditor_uploader.fields
import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
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
                ("Name", models.CharField(max_length=200, verbose_name="نام")),
                ("Image", models.FileField(upload_to="Brands/", verbose_name="تصویر")),
                (
                    "Created_at_g",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ ایجاد میلادی"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "برند ها",
            },
        ),
        migrations.CreateModel(
            name="Category",
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
                    "Name",
                    models.CharField(max_length=200, verbose_name="نام دسته بندی"),
                ),
                ("order", models.IntegerField(default=0, verbose_name="اولویت")),
                ("Active", models.BooleanField(default=True, verbose_name="فعالیت")),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="Products.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "دسته بندی ها",
            },
        ),
        migrations.CreateModel(
            name="Guarantee",
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
                ("Name", models.CharField(max_length=200, verbose_name="نام")),
                (
                    "Image",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="Guarantee/",
                        verbose_name="تصویر",
                    ),
                ),
                ("Created", models.DateTimeField(auto_now_add=True)),
                ("Modified", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "برند ها",
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                ("Slug", models.SlugField(blank=True, max_length=300, null=True)),
                (
                    "RP",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="کد محصول"
                    ),
                ),
                ("Name", models.CharField(max_length=200, verbose_name="نام محصول")),
                (
                    "QrCode",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=Products.models.ProductPath,
                        verbose_name="بارکد محصول",
                    ),
                ),
                (
                    "Url",
                    models.URLField(blank=True, null=True, verbose_name="لینک مستقیم"),
                ),
                (
                    "Discount",
                    Products.models.IntegerRangeField(
                        default=0, verbose_name="درصد تخفیف"
                    ),
                ),
                ("BasePrice", models.IntegerField(default=0, verbose_name="قیمت پایه")),
                ("Rate", models.IntegerField(default=0, verbose_name="امتیاز محصول")),
                (
                    "RateNo",
                    models.IntegerField(default=0, verbose_name="امتیاز دهنده ها"),
                ),
                (
                    "Status",
                    models.IntegerField(
                        choices=[
                            (1, "Created"),
                            (2, "Valid"),
                            (3, "Ban"),
                            (4, "Check"),
                        ],
                        default=2,
                        verbose_name="وضعیت",
                    ),
                ),
                (
                    "Description",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True, verbose_name="توضیحات محصول"
                    ),
                ),
                (
                    "MetaDescription",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("MetaTitle", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "MetaKeywords",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "Visit",
                    models.PositiveIntegerField(default=0, verbose_name="بازدید"),
                ),
                ("Sale", models.PositiveIntegerField(default=0, verbose_name="فروش")),
                (
                    "Created_at_g",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ ایجاد میلادی"
                    ),
                ),
                (
                    "Modified_at_g",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="تاریخ تغییر میلادی"
                    ),
                ),
                (
                    "Created_at_j",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="تاریخ ایجاد شمسی",
                    ),
                ),
                (
                    "Modified_at_j",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="تاریخ تغییر شمسی",
                    ),
                ),
                (
                    "Brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.brand",
                        verbose_name="برند",
                    ),
                ),
                (
                    "Category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.category",
                        verbose_name="دسته بندی",
                    ),
                ),
                (
                    "Guarantee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.guarantee",
                        verbose_name="گارانتی",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "محصولات",
            },
        ),
        migrations.CreateModel(
            name="ProductComment",
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
                    "Date",
                    models.CharField(
                        default=Products.models.Jdate,
                        max_length=100,
                        verbose_name="تاریخ ایجاد شمسی",
                    ),
                ),
                ("Text", models.TextField(max_length=500, verbose_name="متن نظر")),
                ("Rate", models.IntegerField(default=0, verbose_name="امتیاز کامنت")),
                (
                    "Created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ ایجاد میلادی"
                    ),
                ),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.product",
                        verbose_name="محصول",
                    ),
                ),
                (
                    "User",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Users.userinfo",
                        verbose_name="کاربر",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "کامنت های محصول",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                    "RPI",
                    models.CharField(
                        blank=True,
                        default=Products.models.get_random_string,
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "Image",
                    models.FileField(
                        upload_to=Products.models.ProductPathImage, verbose_name="تصویر"
                    ),
                ),
                (
                    "Primary",
                    models.BooleanField(default=False, verbose_name="تصویر اصلی"),
                ),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="image_prd",
                        to="Products.product",
                        verbose_name="محصول",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "تصاویر محصول",
                "ordering": ("-Primary",),
            },
        ),
        migrations.CreateModel(
            name="Variety",
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
                ("RPV", models.CharField(max_length=24, verbose_name="کد تنوع محصول")),
                (
                    "ColorCode",
                    colorfield.fields.ColorField(
                        blank=True,
                        default="#fff",
                        image_field=None,
                        max_length=25,
                        null=True,
                        samples=None,
                        verbose_name="کد رنگ",
                    ),
                ),
                (
                    "ColorName",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="نام رنگ"
                    ),
                ),
                ("Active", models.BooleanField(default=True, verbose_name="تنوع فعال")),
                (
                    "Status",
                    models.IntegerField(
                        choices=[
                            (1, "Created"),
                            (2, "Valid"),
                            (3, "Ban"),
                            (4, "Check"),
                        ],
                        default=2,
                        verbose_name="وضعیت",
                    ),
                ),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variety_product",
                        to="Products.product",
                        verbose_name="محصول",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "تنوعات محصول",
            },
        ),
        migrations.CreateModel(
            name="VarietySub",
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
                    "RPVS",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="تنوع سایز"
                    ),
                ),
                (
                    "Size",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="سایز"
                    ),
                ),
                ("Quantity", models.IntegerField(default=0, verbose_name="موجودی")),
                (
                    "ReserevedQuantity",
                    models.IntegerField(
                        blank=True, default=0, verbose_name=" موجودی رزرو"
                    ),
                ),
                (
                    "Discount",
                    Products.models.IntegerRangeField(
                        default=0, verbose_name="درصد تخفیف"
                    ),
                ),
                (
                    "FinalPrice",
                    models.IntegerField(default=0, verbose_name="قیمت نهایی"),
                ),
                ("OffPrice", models.IntegerField(default=0, verbose_name="مبلغ تخفیف")),
                ("Active", models.BooleanField(default=True, verbose_name="فعال")),
                (
                    "Variety",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="size_var",
                        to="Products.variety",
                        verbose_name="تنوع محصول",
                    ),
                ),
            ],
            options={
                "verbose_name": "Size",
                "verbose_name_plural": "Sizes",
            },
        ),
        migrations.CreateModel(
            name="TopSellToPreview",
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
                    "Name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="نام"
                    ),
                ),
                (
                    "Varities",
                    models.TextField(blank=True, null=True, verbose_name="تنوعات"),
                ),
                (
                    "Created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ ایجاد میلادی"
                    ),
                ),
                ("Active", models.BooleanField(default=True, verbose_name="فعالیت")),
                (
                    "Image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.productimage",
                        verbose_name="تصویر",
                    ),
                ),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.product",
                        verbose_name="محصول",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "محصولات پرفروش",
            },
        ),
        migrations.CreateModel(
            name="Testimotional",
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
                    "Name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="نام"
                    ),
                ),
                (
                    "Created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ ایجاد میلادی"
                    ),
                ),
                ("Active", models.BooleanField(default=True, verbose_name="فعالیت")),
                (
                    "Comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.productcomment",
                        verbose_name="کامنت",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "نمایش نظرات",
            },
        ),
        migrations.CreateModel(
            name="QuantityNotify",
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
                ("Active", models.BooleanField(default=True, verbose_name="فعالیت")),
                ("Created_at", models.DateTimeField(auto_now_add=True)),
                ("Modified", models.DateTimeField(auto_now=True)),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notify_size",
                        to="Products.varietysub",
                        verbose_name="محصول",
                    ),
                ),
            ],
            options={
                "verbose_name": "QuantityNotify",
                "verbose_name_plural": "QuantityNotifies",
            },
        ),
        migrations.CreateModel(
            name="ProductToPreview",
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
                    "Name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="نام"
                    ),
                ),
                (
                    "Varities",
                    models.TextField(blank=True, null=True, verbose_name="تنوعات"),
                ),
                (
                    "Created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ ایجاد میلادی"
                    ),
                ),
                ("Active", models.BooleanField(default=True, verbose_name="فعالیت")),
                (
                    "Image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.productimage",
                        verbose_name="تصویر",
                    ),
                ),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.product",
                        verbose_name="محصول",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "پیشنهادات ویژه",
            },
        ),
        migrations.CreateModel(
            name="ProductTech",
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
                ("Name", models.CharField(max_length=100, verbose_name="نام مشخصه")),
                ("Value", models.CharField(max_length=200, verbose_name="مقدار مشخصه")),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tech_prd",
                        to="Products.product",
                        verbose_name="محصول",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "مشخصات فنی محصول",
            },
        ),
        migrations.CreateModel(
            name="ProductTag",
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
                ("Title", models.CharField(max_length=50, verbose_name="عنوان")),
                (
                    "Product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tag_prd",
                        to="Products.product",
                        verbose_name="محصول",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "برچسب های محصول",
            },
        ),
        migrations.CreateModel(
            name="NotifyNumber",
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
                ("Created_at", models.DateTimeField(auto_now_add=True)),
                ("Modified", models.DateTimeField(auto_now=True)),
                ("Active", models.BooleanField(default=True, verbose_name="فعالیت")),
                (
                    "QN",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="number_notify",
                        to="Products.quantitynotify",
                        verbose_name="Notify",
                    ),
                ),
                (
                    "User",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Users.userinfo",
                        verbose_name="کاربر",
                    ),
                ),
            ],
            options={
                "verbose_name": "NotifyNumber",
                "verbose_name_plural": "NotifyNumbers",
            },
        ),
        migrations.CreateModel(
            name="Filters",
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
                    "Type",
                    models.IntegerField(
                        choices=[
                            (0, "رنگ"),
                            (1, "برند"),
                            (2, "جنس"),
                            (3, "نوع"),
                            (4, "مورد استفاده"),
                            (5, "نوع پاشنه"),
                            (6, "نحوه بسته شدن کفش"),
                            (7, "بند و دستگیره"),
                            (8, "فرم کیف"),
                        ],
                        default=0,
                        verbose_name="نوع",
                    ),
                ),
                ("Name", models.CharField(max_length=200, verbose_name="نام")),
                (
                    "Category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.category",
                        verbose_name="دسته بندی",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "فیلتر ها",
            },
        ),
        migrations.CreateModel(
            name="CommentTip",
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
                ("Type", models.BooleanField(default=True, verbose_name="مثبت/منفی")),
                (
                    "Value",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="مقدار"
                    ),
                ),
                (
                    "Comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_tip",
                        to="Products.productcomment",
                        verbose_name="کامنت",
                    ),
                ),
            ],
            options={
                "verbose_name": "commenttip",
                "verbose_name_plural": "commenttips",
            },
        ),
        migrations.CreateModel(
            name="CategoryToPreview",
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
                    "Name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="نام"
                    ),
                ),
                (
                    "Image",
                    models.FileField(upload_to="Category/", verbose_name="تصویر"),
                ),
                ("Active", models.BooleanField(default=True, verbose_name="فعالیت")),
                (
                    "Category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.category",
                        verbose_name="دسته بندی",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "نمایش دسته بندی ها",
            },
        ),
        migrations.CreateModel(
            name="BrandToPreview",
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
                    "Name",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="نام"
                    ),
                ),
                (
                    "Created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="تاریخ ایجاد میلادی"
                    ),
                ),
                ("Active", models.BooleanField(default=True, verbose_name="فعالیت")),
                (
                    "Brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Products.brand",
                        verbose_name="برند",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "نمایش برند",
            },
        ),
    ]
