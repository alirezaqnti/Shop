from django.db import models
from django.utils.translation import gettext as _
from Users.models import UserInfo
from Main.models import City
from Products.models import VarietySub, Category, IntegerRangeField
import uuid
from django.utils import timezone

import random
import string


def get_random_string():
    letters = string.ascii_uppercase
    result_str = "".join(random.choice(letters) for i in range(6))
    return result_str


class PaymentPortals(models.IntegerChoices):
    sepehrpay = 1
    zarinpal = 2


class paymentChoice(models.IntegerChoices):  # شیوه های پرداخت
    Bank = (1,)
    Zarinpal = (2,)


class CartChoice(models.IntegerChoices):  # وضعیت های سبد خرید
    Created = (0,)
    InProccess = (1,)
    Discarded = (2,)
    Posted = (3,)
    ExchangeRequest = (4,)
    Exchanged = (5,)


class CartProductChoice(models.IntegerChoices):
    Created = (0,)
    Accepted = (1,)
    Declined = (2,)
    Exchanged = (3,)
    Discarded = (4,)
    ExchangeProccess = (5,)


def PurchaseFiles(instance, filename):
    return f"Purchase/{instance.PurchaseTrackNumber}/{filename}"


def CartFiles(instance, filename):
    return "Purchase/{0}/Carts/{1}/{2}".format(
        instance.Purchase.PurchaseTrackNumber, instance.cartNumber, filename
    )


class Cart(models.Model):
    RC = models.CharField(_("کد سفارش"), max_length=24)
    slug = models.SlugField(max_length=500, default=uuid.uuid4)
    User = models.ForeignKey(UserInfo, verbose_name=_(" خریدار"), on_delete=models.CASCADE)
    TotalPrice = models.BigIntegerField(_("مبلغ کل سبد خرید"), default=0)
    Amount = models.BigIntegerField(_("مبلغ کل سفارشات"), default=0)
    TotalDiscount = models.BigIntegerField(_("مجموع تخفیف"), default=0, blank=True, null=True)
    ShippingPrice = models.IntegerField(_("هزینه ارسال"), default=0)
    ShippingPriceAdded = models.BooleanField(default=False)

    UserBankAccountNumber = models.CharField(_("شماره حساب تراکنش"), max_length=50, default="0")
    PaymentWay = models.IntegerField(
        _("روش پرداخت"), default=paymentChoice.Bank, choices=paymentChoice.choices
    )
    PaymentTransactionNumber = models.CharField(
        _("شماره تراکنش بانکی"), max_length=50, default="0"
    )
    PaymentDate = models.CharField(_("تاریخ پرداخت"), max_length=100, blank=True, null=True)
    PurchaseTrackNumber = models.CharField(_("کد پیگیری"), max_length=50, blank=True, null=True)
    policyAccept = models.BooleanField(
        _("تایید شرایط و قوانین"), default=False, blank=True, null=True
    )
    # Return = models.BooleanField(default=True)
    weight = models.IntegerField(_("وزن کل"), default=0)
    Created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        _("وضعیت سبد خرید"), default=CartChoice.Created, choices=CartChoice.choices
    )
    Barcode = models.ImageField(_("تصویر بارکد"), upload_to=PurchaseFiles, null=True, blank=True)
    Vouchered = models.BooleanField(_("کوپن"), default=False)
    VoucherCode = models.CharField(_("کد کوپن"), max_length=8, blank=True, null=True)
    Active = models.BooleanField(_("فعال"), default=True)
    HasReturn = models.BooleanField(_("مورد مرجوعی"), default=False)
    HasCancel = models.BooleanField(_("مورد لغو شده"), default=False)

    class Meta:
        verbose_name = _("سبدخرید")
        verbose_name_plural = _("سبدخرید")


class CartProduct(models.Model):
    slug = models.SlugField(max_length=500, default=uuid.uuid4)
    RCP = models.CharField(_("کد مرسوله"), max_length=50, blank=True, null=True)
    Cart = models.ForeignKey(
        Cart, verbose_name=_("سبدخرید"), on_delete=models.CASCADE, related_name="cartproduct_cart"
    )
    Variety = models.ForeignKey(
        VarietySub,
        verbose_name=_("تنوع محصول"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="size_cart",
    )
    Quantity = models.IntegerField(_("تعداد محصول"), default=1)
    Amount = models.BigIntegerField(_("مبلغ سفارش"), default=0)
    Fee = models.BigIntegerField(_("فی"), default=0)
    discount = models.BigIntegerField(_("مقدار تخفیف"), default=0, blank=True, null=True)
    Offless = models.BigIntegerField(_("قیمت بدون تخفیف"), default=0, blank=True, null=True)
    status = models.IntegerField(
        _("وضعیت سبد خرید"), default=CartProductChoice.Created, choices=CartProductChoice.choices
    )
    Created_At = models.CharField(
        _("تاریخ اضافه شدن به سبد"), max_length=500, blank=True, null=True
    )
    Vouchered = models.BooleanField(_("کوپن"), default=False)
    weight = models.IntegerField(_("وزن کل"), default=0)
    Barcode = models.ImageField(_("تصویر بارکد"), upload_to=CartFiles, blank=True, null=True)
    Active = models.BooleanField(_("فعال"), default=True)
    Created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = _("CartProducts")
        verbose_name = _("CartProduct")

    def delete(self, *args, **kwargs):
        cart = self.Cart
        cart.Amount -= self.Fee
        cart.TotalPrice -= self.Amount
        cart.TotalDiscount -= self.discount
        cart.weight -= self.weight
        cart.save()
        return super(CartProduct, self).delete(*args, **kwargs)

    def exchange(self, *args, **kwargs):
        cart = self.Cart
        cart.Amount -= self.Fee
        cart.TotalPrice -= self.Amount
        cart.TotalDiscount -= self.discount
        cart.weight -= self.weight
        cart.save()
        self.status = CartProductChoice.ExchangeProccess
        return super(CartProduct, self).delete(*args, **kwargs)


class Shipping(models.Model):
    Bike = 0
    Post = 1
    SHIPTYPE = [
        (Bike, "پیک موتوری"),
        (Post, "پست"),
    ]
    Cart = models.OneToOneField(
        Cart,
        verbose_name=_("ادرس خریدار"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="shipping_cart",
    )
    Name = models.CharField(_("نام"), max_length=250)
    Phone = models.CharField(_("شماره تماس"), max_length=12)
    State = models.ForeignKey(
        City, verbose_name=_("استان"), related_name="State", on_delete=models.DO_NOTHING
    )
    City = models.ForeignKey(
        City, verbose_name=_("شهر"), related_name="City", on_delete=models.DO_NOTHING
    )
    Address = models.TextField(_("آدرس"))
    PostalCode = models.CharField(_("کد پستی"), max_length=10)
    No = models.CharField(_("پلاک"), max_length=4)
    Unit = models.CharField(_("واحد"), max_length=4, blank=True, null=True)
    Type = models.IntegerField(_("شیوه ارسال"), default=Post, choices=SHIPTYPE)
    Tips = models.TextField(_("توضیحات"), blank=True, null=True)
    TrackNumber = models.CharField(_("کد رهگیری پستی"), max_length=50, blank=True, null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "مشخصات ارسال"
        verbose_name_plural = "مشخصات ارسال"


class CartPayment(models.Model):
    Slug = models.SlugField(max_length=500, default=uuid.uuid4)
    Auth = models.CharField(max_length=500)
    Cart = models.OneToOneField(
        Cart, verbose_name=_("سبد خرید"), on_delete=models.CASCADE, related_name="payment_cart"
    )
    Amount = models.IntegerField(default=0)
    Ref = models.CharField(max_length=100, blank=True, null=True)
    Status = models.CharField(max_length=10, blank=True, null=True)
    DigitalReceipt = models.CharField(max_length=100, blank=True, null=True)
    Portal = models.IntegerField(
        _("درگاه"), default=PaymentPortals.zarinpal, choices=PaymentPortals.choices
    )
    Verified = models.BooleanField(default=False)
    Response = models.CharField(max_length=400)


class Exchange(models.Model):
    AdminSubmit = "1"
    Inproccess = "2"
    PaymentProccess = "3"
    Done = "4"
    WaitForDeliver = "4"
    STATUS_CHOICE = [
        (AdminSubmit, "جدید"),
        (WaitForDeliver, "در انتظار دریافت"),
        (Inproccess, "درحال انجام"),
        (PaymentProccess, "پردازش پرداخت"),
        (Done, "انجام شده"),
    ]
    RCE = models.CharField(max_length=50, default=get_random_string)
    CP = models.OneToOneField(
        CartProduct,
        verbose_name=_("سفارش"),
        on_delete=models.CASCADE,
        related_name="oldcart_exchange",
    )
    NewCP = models.OneToOneField(
        CartProduct,
        verbose_name=_("سفارش جدید"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="newcart_exchange",
    )
    Status = models.CharField(
        _("وضعیت"), max_length=50, default=AdminSubmit, choices=STATUS_CHOICE
    )
    Report = models.TextField(_("گزارش"))
    Active = models.BooleanField(_("فعال"), default=True)
    Created = models.DateTimeField(auto_now_add=True)
    Modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _("تعویض محصول")

    def __str__(self):
        return self.RCE


class WishList(models.Model):
    slug = models.SlugField(max_length=500, default=uuid.uuid4)
    RW = models.CharField(_("کد آیتم مورد علاقه"), max_length=50, blank=True, null=True)
    User = models.ForeignKey(UserInfo, verbose_name=_(" خریدار"), on_delete=models.CASCADE)
    Variety = models.ForeignKey(
        VarietySub, verbose_name=_("تنوع محصول"), on_delete=models.CASCADE, blank=True, null=True
    )
    Created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("مورد علاقه ها")
        verbose_name_plural = _("مورد علاقه ها")


class Coupon(models.Model):
    Cat = "1"
    Invoice = "2"

    TYPE_CHOICES = [(Cat, "دسته بندی"), (Invoice, "فاکتور")]
    Category = models.ForeignKey(
        Category,
        verbose_name=_("دسته بندی"),
        on_delete=models.CASCADE,
        related_name="coupon_cat",
        blank=True,
        null=True,
    )
    Code = models.CharField(_("کوپن تخفیف"), max_length=6, default=get_random_string)
    Type = models.CharField(_("نوع"), max_length=50, default=Invoice, choices=TYPE_CHOICES)
    Discount = IntegerRangeField(_("درصد تخفیف"), default=0, min_value=0, max_value=100)
    MaxPrice = models.PositiveIntegerField(_("حداکثر تخفیف"), default=0)
    MaxUse = models.PositiveIntegerField(_("حداکثر استفاده کاربر"), default=1)
    Time = models.DateTimeField(_("زمان"), auto_now=False, default=timezone.now)
    Active = models.BooleanField(_("فعال"), default=True)
    Created = models.DateTimeField(auto_now_add=True)
    Modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("کوپن تخفیف")
        verbose_name_plural = _("کوپن تخفیف")

    def __str__(self):
        return self.Code


class CouponUser(models.Model):
    Coupon = models.ForeignKey(
        Coupon, verbose_name=_("کوپن"), on_delete=models.CASCADE, related_name="user_coupon"
    )
    User = models.ForeignKey(UserInfo, verbose_name=_(" خریدار"), on_delete=models.CASCADE)
    Usage = models.PositiveIntegerField(_("تعداد استفاده کاربر"), default=0)
    Amount = models.PositiveIntegerField(_("مبلغ"), default=0)
    Created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("CouponUser")
        verbose_name_plural = _("CouponUsers")

    def __str__(self):
        return self.User.Name


class WheelOfFortune(models.Model):
    Date = models.DateTimeField(_("زمان"), auto_now=False, default=timezone.now)
    MaxUse = models.PositiveIntegerField(_("حداکثر استفاده کاربر"), default=1)
    Created_At = models.DateTimeField(auto_now_add=True)
    Modified_At = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name_plural = _("گردونه شانس")

    def __str__(self):
        return "گردونه شماره " + str(self.pk)


class FortunePrize(models.Model):
    RFP = models.CharField(max_length=50, blank=True, null=True, default=get_random_string)
    Title = models.CharField(_("عنوان"), max_length=200, null=True, blank=True)
    Wheel = models.ForeignKey(
        WheelOfFortune,
        verbose_name=_("گردونه"),
        on_delete=models.CASCADE,
        related_name="prize_wheel",
    )
    Coupon = models.ForeignKey(
        Coupon,
        verbose_name=_("کوپن"),
        on_delete=models.CASCADE,
        related_name="fortune_coupon",
        blank=True,
        null=True,
    )
    Price = models.PositiveIntegerField(_("مبلغ"), default=0)
    Null = models.BooleanField(_("پوچ"), default=False)
    Created_At = models.DateTimeField(auto_now_add=True)
    Modified_At = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(_("فعال"), default=True)

    def __str__(self):
        return self.Title


class FortuneUser(models.Model):
    Wheel = models.ForeignKey(
        WheelOfFortune,
        verbose_name=_("گردونه"),
        on_delete=models.CASCADE,
        related_name="user_wheel",
    )
    Prize = models.ForeignKey(
        FortunePrize,
        verbose_name=_("جایزه"),
        on_delete=models.CASCADE,
        related_name="user_prize",
    )
    User = models.ForeignKey(UserInfo, verbose_name=_(" خریدار"), on_delete=models.CASCADE)
    Usage = models.PositiveIntegerField(_("تعداد استفاده کاربر"), default=0)
    Created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _("برندگان گردونه")

    def __str__(self):
        return self.User.Name


class PurchaseTrack(models.Model):
    New = "1"
    Proccess = "2"
    Done = "3"
    STATUS_CHOICE = [
        (New, "جدید"),
        (Proccess, "در حال پردازش"),
        (Done, "انجام شده"),
    ]

    Cart = models.ForeignKey(
        Cart, verbose_name=_("سبدخرید"), on_delete=models.CASCADE, related_name="track_cart"
    )
    User = models.ForeignKey(UserInfo, verbose_name=_(" خریدار"), on_delete=models.CASCADE)
    Phone = models.CharField(_("شماره تماس"), max_length=11)
    Describtion = models.TextField(_("توضیحات"), blank=True, null=True)
    Report = models.TextField(_("گزارش"), blank=True, null=True)
    Status = models.CharField(_("وضعیت"), max_length=50, default=New, choices=STATUS_CHOICE)
    Created_At = models.DateTimeField(auto_now_add=True)
    Modified_At = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _("پیگیری سفارش")

    def __str__(self):
        return self.Cart.RC
