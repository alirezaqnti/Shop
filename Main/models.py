import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from Products.models import VarietySub, Product
from Users.models import UserInfo
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import random
import string
from Users.models import GenderType, UserInfo


def get_random_string():
    letters = string.ascii_uppercase
    result_str = "".join(random.choice(letters) for i in range(6))
    return result_str


def Generate():
    return random.randint(100000, 999999)


class UserEntity(models.IntegerChoices):
    Admin = 0
    User = 1
    Provider = 2


class City(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return self.title


class CodeReg(models.Model):
    Code = models.CharField(_("کد"), max_length=6, default=Generate)
    Phone = models.CharField(_("شماره همراه"), max_length=50)
    Email = models.CharField(_("ایمیل"), max_length=50)
    Active = models.BooleanField(_("وضعیت"), default=True)
    Created_At = models.DateTimeField(
        _("تاریخ ایجاد"), auto_now=False, default=timezone.now
    )

    class Meta:
        verbose_name_plural = _("CodeRegs")

    def __str__(self):
        return self.Code


class ImageBox(models.Model):
    Image = "1"
    Data = "2"
    Link = "3"
    TYPE_CHOICES = [
        (Image, "تصویر"),
        (Data, "مستقل"),
        (Link, "تصویر با لینک"),
    ]

    SLIDER = "1"
    BIGBOX = "2"
    TRIPLEBOX = "3"

    PLACEMENT_CHOICE = [
        (SLIDER, "اسلایدر"),
        (BIGBOX, "باکس میانی"),
        (TRIPLEBOX, "باکس سه گانه"),
    ]

    RS = models.CharField(
        max_length=50, blank=True, null=True, default=get_random_string
    )
    Type = models.CharField(
        _("نوع"), max_length=50, default=Image, choices=TYPE_CHOICES
    )
    Placement = models.CharField(
        _("جایگاه"), max_length=50, default=SLIDER, choices=PLACEMENT_CHOICE
    )
    Image_H = models.ImageField(_("تصویر افقی"), upload_to="Slider/", max_length=100)
    Image_V = models.ImageField(_("تصویر عمودی"), upload_to="Slider/", max_length=100)
    Url = models.URLField(_("لینک"), max_length=250, blank=True, null=True)
    Rich = RichTextUploadingField(null=True, blank=True)
    Order = models.PositiveIntegerField(_("اولویت"), default=0)
    Created = models.DateTimeField(_("تاریخ"), auto_now_add=True)
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name_plural = _("باکس تصاویر")


class ContactUs(models.Model):
    Name = models.CharField(_("نام"), max_length=100)
    Email = models.EmailField(_("ایمیل"), max_length=254)
    Phone = models.CharField(_("تلفن همراه"), max_length=13)
    Text = models.TextField(_("متن"), max_length=500)
    Subject = models.CharField(_("موضوع"), max_length=50)
    Created = models.DateTimeField(_("تاریخ"), auto_now_add=True)

    class Meta:
        verbose_name = _("تماس باما")
        verbose_name_plural = _("تماس باما")

    def __str__(self):
        return self.Name


class Offers(models.Model):
    POPUP = "1"
    DISCOUNT = "2"
    SELECTIVE = "3"
    TYPE_CHOICES = [
        (POPUP, "پاپ اپ"),
        (DISCOUNT, "تخفبف"),
        (SELECTIVE, "انتخابی"),
    ]
    Sub = models.ForeignKey(
        VarietySub, verbose_name=_("تنوع محصول"), on_delete=models.CASCADE
    )
    Product = models.ForeignKey(
        Product,
        verbose_name=_("محصول"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    Type = models.CharField(
        _("نوع"), max_length=50, default=POPUP, choices=TYPE_CHOICES
    )
    Created = models.DateTimeField(_("تاریخ"), auto_now_add=True)
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name_plural = _("آفر ها")

    def __str__(self):
        return self.Product.Name


class Staff(models.Model):
    SuperUser = "0"
    Admin = "1"
    ContentCreator = "2"
    Warehouse = "3"
    Accountant = "4"
    Seo = "5"
    POSITION_CHOICE = [
        (SuperUser, "ابر یوزر"),
        (Admin, "ادمین"),
        (ContentCreator, "تولید کننده محتوا"),
        (Warehouse, "انباردار"),
        (Accountant, "حسابدار"),
        (Seo, "سئوکار"),
    ]
    slug = models.SlugField(unique=True, blank=True, null=True)
    Email = models.EmailField(_("ایمیل"), max_length=254)
    Phone = models.CharField(_("شماره تماس"), max_length=13)
    Gender = models.IntegerField(
        _("جنسیت"), default=GenderType.Female, choices=GenderType.choices
    )
    Password = models.CharField(_("رمز عبور"), max_length=250, blank=True, null=True)
    key = models.BinaryField(blank=True, null=True, max_length=200)
    Name = models.CharField(_("نام"), max_length=100)
    Position = models.CharField(
        _("موقعیت شغلی"), max_length=50, default=Admin, choices=POSITION_CHOICE
    )
    Created_At = models.DateTimeField(auto_now_add=True)
    Modified_At = models.DateTimeField(auto_now=True)
    Last_Login = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = "پرسنل"

    def __str__(self):
        return self.Name


class Address(models.Model):  # جدول مربوط به ادرس های کاربر
    User = models.ForeignKey(UserInfo, verbose_name=_(""), on_delete=models.CASCADE)
    Title = models.CharField(_("عنوان آدرس"), max_length=100)  # عنوان آدرس
    Name = models.CharField(_("نام"), max_length=100)  # نام گیرنده
    Phone = models.CharField(_("شماره همراه"), max_length=11)  # شماره تلفن گیرنده
    State = models.ForeignKey(
        City,
        verbose_name=_("استان"),
        related_name="state_city",
        on_delete=models.CASCADE,
    )  # استان
    City = models.ForeignKey(
        City, verbose_name=_("شهر"), related_name="city_city", on_delete=models.CASCADE
    )  # شهر
    PostalAddress = models.CharField(_("آدرس پستی"), max_length=500)  # ادرس پستی
    PostalCode = models.CharField(_("کد پستی"), max_length=10)  # کد پستی
    Number = models.CharField(_("پلاک"), max_length=4)  # پلاک
    Unit = models.CharField(_("واحد"), max_length=5, blank=True)  # واحد
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name_plural = "آدرس"

    def toJson(self):
        return {
            "addressTitle": self.Title,
            "User": self.User.Name,
            "User_id": self.User.pk,
            "Name": self.Name,
            "Phone": self.Phone,
            "State": self.State,
            "City": self.City,
            "PostalAddress": self.PostalAddress,
            "PostalCode": self.PostalCode,
            "Number": self.Number,
            "Unit": self.Unit,
            "Active": self.Active,
        }
