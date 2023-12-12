from core.settings import BASE_DIR, MEDIA_ROOT
from django.db import models
from django.utils.translation import gettext as _
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
import jdatetime
from colorfield.fields import ColorField
from Users.models import UserInfo
import random, string


def get_random_string():
    letters = string.ascii_uppercase
    result_str = "".join(random.choice(letters) for i in range(6))
    return result_str


def ProductPath(instance, filename):
    return "Products/" + "%s/%s" % (instance.RP, filename)


def ProductPathImage(instance, filename):
    return "Products/" + "%s/%s" % (instance.Product.RP, filename)


def Jdate():
    return jdatetime.datetime.today().strftime("%Y-%m-%d")


class ProductStat(models.IntegerChoices):
    created = (1,)
    valid = (2,)
    ban = (3,)
    check = (4,)


class IntegerRangeField(models.IntegerField):
    def __init__(
        self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs
    ):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"min_value": self.min_value, "max_value": self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Category(MPTTModel):
    Name = models.CharField(_("نام دسته بندی"), max_length=200)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    order = models.IntegerField(_("اولویت"), default=0)
    Active = models.BooleanField(_("فعالیت"), default=True)

    class Meta:
        verbose_name_plural = _("دسته بندی ها")

    def __str__(self):
        return self.Name

    def to_json(self):
        return {
            "id": self.id,
            "Name": self.Name,
            "parent_id": str(self.parent_id),
            "level": self.level,
            "order": self.order,
        }


class Brand(models.Model):
    Name = models.CharField(_("نام"), max_length=200)
    Image = models.FileField(_("تصویر"), upload_to="Brands/", max_length=100)
    Created_at_g = models.DateTimeField(_("تاریخ ایجاد میلادی"), auto_now_add=True)

    class Meta:
        verbose_name_plural = _("برند ها")

    def __str__(self):
        return self.Name


class Guarantee(models.Model):
    Name = models.CharField(_("نام"), max_length=200)
    Image = models.FileField(
        _("تصویر"), upload_to="Guarantee/", max_length=100, blank=True, null=True
    )
    Created = models.DateTimeField(auto_now_add=True)
    Modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _("گارانتی")

    def __str__(self):
        return self.Name


class Product(models.Model):
    Slug = models.SlugField(max_length=300, blank=True, null=True)
    Category = models.ForeignKey(
        Category, verbose_name=_("دسته بندی"), on_delete=models.CASCADE
    )
    Brand = models.ForeignKey(
        Brand, verbose_name=_("برند"), on_delete=models.CASCADE, blank=True, null=True
    )
    Guarantee = models.ForeignKey(
        Guarantee,
        verbose_name=_("گارانتی"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    RP = models.CharField(_("کد محصول"), max_length=50, blank=True, null=True)
    Name = models.CharField(_("نام محصول"), max_length=200)
    QrCode = models.FileField(
        _("بارکد محصول"), upload_to=ProductPath, max_length=100, blank=True, null=True
    )
    Url = models.URLField(_("لینک مستقیم"), max_length=200, blank=True, null=True)
    Discount = IntegerRangeField(_("درصد تخفیف"), default=0, min_value=0, max_value=100)
    BasePrice = models.BigIntegerField(_("قیمت پایه"), default=0)
    Rate = models.IntegerField(_("امتیاز محصول"), default=0)
    RateNo = models.IntegerField(_("امتیاز دهنده ها"), default=0)
    Status = models.IntegerField(
        _("وضعیت"), default=ProductStat.valid, choices=ProductStat.choices
    )
    Description = RichTextUploadingField(_("توضیحات محصول"), blank=True, null=True)
    Demo = models.TextField(_("دمو توضیحات محصول"), blank=True, null=True)
    MetaDescription = models.CharField(max_length=100, blank=True, null=True)
    MetaTitle = models.CharField(max_length=100, blank=True, null=True)
    MetaKeywords = models.CharField(max_length=200, blank=True, null=True)
    Visit = models.PositiveIntegerField(_("بازدید"), default=0)
    Sale = models.PositiveIntegerField(_("فروش"), default=0)
    Created_at_g = models.DateTimeField(_("تاریخ ایجاد میلادی"), auto_now_add=True)
    Modified_at_g = models.DateTimeField(
        _("تاریخ تغییر میلادی"), auto_now=True, blank=True, null=True
    )
    Created_at_j = models.CharField(
        _("تاریخ ایجاد شمسی"), max_length=50, blank=True, null=True
    )
    Modified_at_j = models.CharField(
        _("تاریخ تغییر شمسی"), max_length=50, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = _("محصولات")

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        return super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    RPI = models.CharField(
        max_length=50, blank=True, null=True, default=get_random_string
    )
    Product = models.ForeignKey(
        Product,
        verbose_name=_("محصول"),
        on_delete=models.CASCADE,
        related_name="image_prd",
    )
    Image = models.FileField(_("تصویر"), upload_to=ProductPathImage, max_length=100)
    Primary = models.BooleanField(_("تصویر اصلی"), default=False)

    class Meta:
        verbose_name_plural = _("تصاویر محصول")
        ordering = ("-Primary",)


class ProductTech(models.Model):
    Product = models.ForeignKey(
        Product,
        verbose_name=_("محصول"),
        on_delete=models.CASCADE,
        related_name="tech_prd",
    )
    Name = models.CharField(_("نام مشخصه"), max_length=100)
    Value = models.CharField(_("مقدار مشخصه"), max_length=200)

    class Meta:
        verbose_name_plural = _("مشخصات فنی محصول")

    def __str__(self):
        return self.Name


class Filters(models.Model):
    Category = models.ForeignKey(
        Category,
        verbose_name=_("دسته بندی"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Name = models.CharField(_("نام"), max_length=200)

    class Meta:
        verbose_name_plural = _("فیلتر ها")

    def __str__(self):
        return self.Name


class FilterValue(models.Model):
    Filter = models.ForeignKey(
        Filters,
        verbose_name=_("فیلتر"),
        related_name="val_filter",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Title = models.CharField(_("عنوان"), max_length=200)

    class Meta:
        verbose_name = _("FilterValue")
        verbose_name_plural = _("FilterValues")

    def __str__(self):
        return self.Title


class ProductFilter(models.Model):
    Product = models.ForeignKey(
        Product,
        verbose_name=_("محصول"),
        related_name="fil_prd",
        on_delete=models.CASCADE,
    )
    Filter = models.ForeignKey(
        FilterValue,
        verbose_name=_("فیلتر"),
        related_name="fil_fil",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("productfilter")
        verbose_name_plural = _("productfilters")

    def __str__(self):
        return str(self.pk)


class Variety(models.Model):
    Product = models.ForeignKey(
        Product,
        verbose_name=_("محصول"),
        on_delete=models.CASCADE,
        related_name="variety_product",
    )
    RPV = models.CharField(_("کد تنوع محصول"), max_length=24)
    ColorCode = ColorField(_("کد رنگ"), default="#fff", blank=True, null=True)
    ColorName = models.CharField(_("نام رنگ"), max_length=100, blank=True, null=True)
    Active = models.BooleanField(_("تنوع فعال"), default=True)
    Status = models.IntegerField(
        _("وضعیت"), default=ProductStat.valid, choices=ProductStat.choices
    )

    class Meta:
        verbose_name_plural = _("تنوعات محصول")

    def __str__(self):
        return self.RPV


class VarietySub(models.Model):
    RPVS = models.CharField(_("تنوع سایز"), max_length=50, blank=True, null=True)
    Variety = models.ForeignKey(
        Variety,
        verbose_name=_("تنوع محصول"),
        on_delete=models.CASCADE,
        related_name="size_var",
    )
    Size = models.CharField(_("سایز"), max_length=50, blank=True, null=True)
    Quantity = models.IntegerField(_("موجودی"), default=0)
    ReserevedQuantity = models.PositiveIntegerField(
        _(" موجودی رزرو"), blank=True, default=0
    )
    Discount = IntegerRangeField(_("درصد تخفیف"), default=0, min_value=0, max_value=100)
    FinalPrice = models.BigIntegerField(_("قیمت نهایی"), default=0)
    OffPrice = models.IntegerField(_("مبلغ تخفیف"), default=0)
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name = _("Size")
        verbose_name_plural = _("Sizes")

    def __str__(self):
        return self.RPVS

    def toJson(self):
        Var = self.Variety
        Pr = Var.Product
        Img = ProductImage.objects.filter(Product=Pr, Primary=True).first()
        if Pr.Brand:
            Brand = Pr.Brand.Name
        else:
            Brand = None
        return {
            "Image": str(Img.Image),
            "RP": Pr.Slug,
            "RPVS": self.RPVS,
            "Size": self.Size,
            "Discount": self.Discount,
            "FinalPrice": self.FinalPrice,
            "Name": self.Name,
            "Name_": Pr.Name,
            "ColorCode": Var.ColorCode,
            "Brand": Brand,
        }


class ProductComment(models.Model):
    Product = models.ForeignKey(
        Product,
        verbose_name=_("محصول"),
        on_delete=models.CASCADE,
        related_name="cm_prd",
    )
    User = models.ForeignKey(
        UserInfo, verbose_name=_("کاربر"), on_delete=models.CASCADE
    )
    Date = models.CharField(_("تاریخ ایجاد شمسی"), max_length=100, default=Jdate)
    Text = models.TextField(_("متن نظر"), max_length=500)
    Rate = models.IntegerField(_("امتیاز کامنت"), default=0)
    Created_at = models.DateTimeField(_("تاریخ ایجاد میلادی"), auto_now_add=True)

    class Meta:
        verbose_name_plural = _("کامنت های محصول")

    def __str__(self):
        return self.Product.Name

    def toJson(self):
        return {
            "Product": self.Product_id,
            "User": self.User_id,
            "User_Name": self.User.Name,
            "Date": self.Date,
            "Text": self.Text,
            "Rate": self.Rate,
            "RateRange": range(self.Rate),
            "Created_at ": str(self.Created_at),
        }


class CommentTip(models.Model):
    Comment = models.ForeignKey(
        ProductComment,
        verbose_name=_("کامنت"),
        related_name="comment_tip",
        on_delete=models.CASCADE,
    )
    Type = models.BooleanField(_("مثبت/منفی"), default=True)
    Value = models.CharField(_("مقدار"), max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("commenttip")
        verbose_name_plural = _("commenttips")


class ProductTag(models.Model):
    Product = models.ForeignKey(
        Product,
        verbose_name=_("محصول"),
        on_delete=models.CASCADE,
        related_name="tag_prd",
    )
    Title = models.CharField(_("عنوان"), max_length=50)

    class Meta:
        verbose_name_plural = _("برچسب های محصول")

    def __str__(self):
        return self.Title


class BrandToPreview(models.Model):
    Brand = models.ForeignKey(Brand, verbose_name=_("برند"), on_delete=models.CASCADE)
    Name = models.CharField(_("نام"), null=True, blank=True, max_length=100)
    Created_at = models.DateTimeField(_("تاریخ ایجاد میلادی"), auto_now_add=True)
    Active = models.BooleanField(_("فعالیت"), default=True)

    class Meta:
        verbose_name_plural = _("نمایش برند")

    def __str__(self):
        return self.Name


class ProductToPreview(models.Model):
    Name = models.CharField(_("نام"), null=True, blank=True, max_length=100)
    Product = models.ForeignKey(
        Product, verbose_name=_("محصول"), on_delete=models.CASCADE
    )
    Image = models.ForeignKey(
        ProductImage,
        verbose_name=_("تصویر"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Varities = models.TextField(_("تنوعات"), null=True, blank=True)
    Created_at = models.DateTimeField(_("تاریخ ایجاد میلادی"), auto_now_add=True)
    Active = models.BooleanField(_("فعالیت"), default=True)

    class Meta:
        verbose_name_plural = _("پیشنهادات ویژه")

    def __str__(self):
        return self.Name


class TopSellToPreview(models.Model):
    Name = models.CharField(_("نام"), null=True, blank=True, max_length=100)
    Product = models.ForeignKey(
        Product, verbose_name=_("محصول"), on_delete=models.CASCADE
    )
    Image = models.ForeignKey(
        ProductImage,
        verbose_name=_("تصویر"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Varities = models.TextField(_("تنوعات"), null=True, blank=True)
    Created_at = models.DateTimeField(_("تاریخ ایجاد میلادی"), auto_now_add=True)
    Active = models.BooleanField(_("فعالیت"), default=True)

    class Meta:
        verbose_name_plural = _("محصولات پرفروش")

    def __str__(self):
        return self.Name


class CategoryToPreview(models.Model):
    Name = models.CharField(_("نام"), null=True, blank=True, max_length=100)
    Category = models.ForeignKey(
        Category, verbose_name=_("دسته بندی"), on_delete=models.CASCADE
    )
    Image = models.FileField(_("تصویر"), upload_to="Category/", max_length=100)
    Active = models.BooleanField(_("فعالیت"), default=True)

    class Meta:
        verbose_name_plural = _("نمایش دسته بندی ها")

    def __str__(self):
        return self.Name


class Testimotional(models.Model):
    Comment = models.ForeignKey(
        ProductComment, verbose_name=_("کامنت"), on_delete=models.CASCADE
    )
    Name = models.CharField(_("نام"), null=True, blank=True, max_length=100)
    Created_at = models.DateTimeField(_("تاریخ ایجاد میلادی"), auto_now_add=True)
    Active = models.BooleanField(_("فعالیت"), default=True)

    class Meta:
        verbose_name_plural = _("نمایش نظرات")

    def __str__(self):
        return self.Name


class QuantityNotify(models.Model):
    Product = models.ForeignKey(
        VarietySub,
        verbose_name=_("محصول"),
        on_delete=models.CASCADE,
        related_name="notify_size",
    )
    Active = models.BooleanField(_("فعالیت"), default=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("QuantityNotify")
        verbose_name_plural = _("QuantityNotifies")


class NotifyNumber(models.Model):
    QN = models.ForeignKey(
        QuantityNotify,
        verbose_name=_("Notify"),
        on_delete=models.CASCADE,
        related_name="number_notify",
    )
    User = models.ForeignKey(
        UserInfo, verbose_name=_("کاربر"), on_delete=models.CASCADE
    )
    Created_at = models.DateTimeField(auto_now_add=True)
    Modified = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(_("فعالیت"), default=True)

    class Meta:
        verbose_name = _("NotifyNumber")
        verbose_name_plural = _("NotifyNumbers")
