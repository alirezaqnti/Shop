import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from Products.models import Variety, VarietySub
from Users.models import UserInfo
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import random
import string
from Users.models import GenderType


def get_random_string():
    letters = string.ascii_uppercase
    result_str = "".join(random.choice(letters) for i in range(6))
    return result_str


def Generate():
    return random.randint(100000, 999999)


class Shortener(models.Model):
    Real = models.CharField(_("مسیر اصلی"), max_length=400)
    Short = models.URLField(_("لینک کوتاه"), max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _("Shortener")
        verbose_name_plural = _("Shorteners")

    def __str__(self):
        return self.Short


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
    Created_At = models.DateTimeField(_("تاریخ ایجاد"), auto_now=False, default=timezone.now)

    class Meta:
        verbose_name_plural = _("CodeRegs")

    def __str__(self):
        return self.Code


class Slider(models.Model):
    Wheel = "0"
    Image = "1"
    Data = "2"
    Link = "3"
    TYPE_CHOICES = [
        (Wheel, "گردونه شانس"),
        (Image, "تصویر"),
        (Data, "مستقل"),
        (Link, "تصویر با لینک"),
    ]

    RS = models.CharField(max_length=50, blank=True, null=True, default=get_random_string)
    Type = models.CharField(_("نوع"), max_length=50, default=Image, choices=TYPE_CHOICES)
    Image_H = models.ImageField(_("تصویر افقی"), upload_to="Slider/", max_length=100)
    Image_V = models.ImageField(_("تصویر عمودی"), upload_to="Slider/", max_length=100)
    Url = models.URLField(_("لینک"), max_length=250, blank=True, null=True)
    Rich = RichTextUploadingField(null=True, blank=True)
    Order = models.PositiveIntegerField(_("اولویت"), default=0)
    Created = models.DateTimeField(_("تاریخ"), auto_now_add=True)

    class Meta:
        verbose_name = _("اسلایدر")
        verbose_name_plural = _("اسلایدر")


class TwinBox(models.Model):
    Image = models.ImageField(_("تصویر"), upload_to="TwinBox/", max_length=100)
    Order = models.PositiveIntegerField(_("اولویت"), default=0)
    Url = models.URLField(_("لینک"), max_length=250)

    class Meta:
        verbose_name = _("باکس های دوقلو")
        verbose_name_plural = _("باکس های دوقلو")


class BigSellBox(models.Model):
    Variety = models.ForeignKey(
        VarietySub, verbose_name=_("تنوع محصول"), on_delete=models.CASCADE, blank=True, null=True
    )
    Image = models.ImageField(_("تصویر"), upload_to="BigSellBox/", max_length=100)
    Text = models.CharField(_("متن"), max_length=200)
    Url = models.URLField(_("لینک"), max_length=250)

    class Meta:
        verbose_name = _("باکس بزرگ")
        verbose_name_plural = _("باکس بزرگ")

    def __str__(self):
        return self.Variety.Variety.Product.Name


class DiscountBox(models.Model):
    Variety = models.ForeignKey(
        VarietySub, verbose_name=_("تنوع محصول"), on_delete=models.CASCADE, blank=True, null=True
    )
    Time = models.DateTimeField(_("زمان"), auto_now=False, default=timezone.now)
    Text = models.CharField(_("متن"), max_length=200)
    Image = models.ImageField(_("تصویر"), upload_to="DiscountBox/", max_length=100)

    class Meta:
        verbose_name = _("باکس تخفیف ویژه")
        verbose_name_plural = _("باکس تخفیف ویژه")

    def __str__(self):
        return self.Variety.Variety.Product.Name


class OfferBox(models.Model):
    Variety = models.ForeignKey(
        VarietySub, verbose_name=_("تنوع محصول"), on_delete=models.CASCADE, blank=True, null=True
    )
    Time = models.DateTimeField(_("زمان"), auto_now=False, default=timezone.now)
    Text = models.CharField(_("متن"), max_length=200)
    Image = models.ImageField(_("تصویر"), upload_to="OfferBox/", max_length=100)

    class Meta:
        verbose_name = _("باکس پیشنهاد ویزه")
        verbose_name_plural = _("باکس پیشنهاد ویزه")

    def __str__(self):
        return self.Variety.Variety.Product.Name


class MiniBox(models.Model):
    Image = models.ImageField(
        _("تصویر"), upload_to="MiniBox/", max_length=100, blank=True, null=True
    )
    Text = models.CharField(_("متن"), max_length=200)
    Url = models.URLField(_("لینک"), max_length=250)

    class Meta:
        verbose_name = _("باکس لیست تخفیف")
        verbose_name_plural = _("باکس لیست تخفیف")


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


class QuickOffer(models.Model):
    Variety = models.ForeignKey(VarietySub, verbose_name=_("تنوع محصول"), on_delete=models.CASCADE)
    Image = models.ImageField(
        _("تصویر"), upload_to="QuickOffer/", max_length=100, blank=True, null=True
    )
    Url = models.URLField(_("لینک"), max_length=250, blank=True, null=True)
    Name = models.CharField(_("نام"), max_length=200, blank=True, null=True)
    Created = models.DateTimeField(_("تاریخ"), auto_now_add=True)
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name_plural = _("آفر های سریع")

    def __str__(self):
        return self.Name


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
    Gender = models.IntegerField(_("جنسیت"), default=GenderType.Female, choices=GenderType.choices)
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
