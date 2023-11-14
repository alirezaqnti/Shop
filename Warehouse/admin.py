from django.shortcuts import render, redirect
from django.contrib import admin, messages
from django.urls import path
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from .models import (
    Cart,
    CartChoice,
    CartProductChoice,
    CartProduct,
    WishList,
    Shipping,
    Coupon,
    CouponUser,
    FortunePrize,
    WheelOfFortune,
    FortuneUser,
    Exchange,
    PurchaseTrack,
)
from Products.models import VarietySub
from Main.views import SendSMS
from Main.models import City, Staff
from jalali_date.admin import ModelAdminJalaliMixin
from .views import NewPRo
from django.db import transaction
import math


class CartProductInline(admin.TabularInline):
    model = CartProduct


class ShippingInline(admin.TabularInline):
    model = Shipping
    max_num = 1


admin.site.register(CouponUser)


@admin.register(PurchaseTrack)
class PurchaseTrackAdmin(admin.ModelAdmin):
    """Admin View for PurchaseTrack"""

    list_display = [
        "Cart",
        "User",
        "Phone",
        "Status",
    ]
    search_fields = ("Cart__RC", "Phone")
    ordering = ("-Created_At",)


class FortunePrizeInline(admin.TabularInline):
    model = FortunePrize
    min_num = 6
    extra = 0
    readonly_fields = ["RFP", "Coupon"]


@admin.register(WheelOfFortune)
class WheelOfFortuneAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_filter = ("Active",)
    inlines = [
        FortunePrizeInline,
    ]
    readonly_fields = ["Created_At", "Modified_At"]
    ordering = ("Created_At",)


@admin.register(FortuneUser)
class FortuneUserAdmin(admin.ModelAdmin):
    """Admin View for FortuneUser"""

    list_display = [
        "Wheel",
        "Prize",
        "User",
    ]
    list_filter = ("Wheel",)
    readonly_fields = [
        "Wheel",
        "Prize",
        "User",
    ]
    search_fields = ("Prize__RFP", "User__Phone")
    ordering = ("Created",)


@admin.register(Coupon)
class CouponAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        "Code",
        "Type",
        "Active",
        "Time",
        "Created",
    ]
    list_filter = ("Type", "Active")
    search_fields = ("Code",)
    ordering = ("-Created",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    change_form_template = "admin/Cart.html"
    list_display = ("User", "RC", "TotalPrice", "status")
    search_fields = ("RC", "User__Phone")
    inlines = [CartProductInline, ShippingInline]
    ordering = ("Created",)
    list_filter = ["status"]

    def change_view(self, request, object_id):
        Cr = (
            Cart.objects.filter(pk=object_id)
            .prefetch_related("cartproduct_cart", "shipping_cart")
            .first()
        )
        User = Cr.User
        try:
            Ship = Cr.shipping_cart
        except:
            Ship = False
        cities = City.objects.filter(parent=0)
        # CPs = Cr.cartproduct_cart.filter()
        context = self.get_changeform_initial_data(request)
        context["Cart"] = Cr
        context["City"] = cities
        context.update(self.admin_site.each_context(request))
        if request.POST:
            with transaction.atomic():
                if "AddressBtn" in request.POST:
                    if Cr.status == 1:
                        State = request.POST["State"]
                        Ci = request.POST["City"]
                        PostalCode = request.POST["PostalCode"]
                        No = request.POST["No"]
                        Unit = request.POST["Unit"]
                        Address = request.POST["Address"]
                        Ship.State_id = State
                        Ship.City_id = Ci
                        Ship.Address = Address
                        Ship.PostalCode = PostalCode
                        Ship.No = No
                        Ship.Unit = Unit
                        Ship.save()
                    else:
                        messages.error(request, "امکان تغییر آدرس وجود ندارد")
            with transaction.atomic():
                if "TrackNumberBtn" in request.POST:
                    TrackNumber = request.POST["TrackNumber"]
                    Ship.TrackNumber = TrackNumber
                    Ship.save()
                    if Ship.Type == 1:
                        Text = f"""
                            {User.Name} عزیز 
                            سفارش شماره {Cr.RC} ارسال شده است 
                            با کد رهگیری زیر می توانید از اخرین وضعیت سفارشات خود در وبسایت شرکت پست مطلع شوید
                            کد رهگیری: {TrackNumber}
                            
                        """
                    else:
                        Text = f"""
                            {User.Name} عزیز 
                            سفارش شماره {Cr.RC} ارسال شده است و تا ساعات آینده به دست شما خواهد رسید

                        """
                    SendSMS(User.Phone, Text)
                    Cr.status = CartChoice.Posted
                    Cr.save()
            with transaction.atomic():
                if "NewCPForm" in request.POST:
                    RPVS = request.POST["RPVS"]
                    CP = request.POST["CP"]
                    Quantity = int(request.POST["Quantity"])
                    O_CP = CartProduct.objects.get(RCP=CP)
                    CR = O_CP.Cart
                    var = VarietySub.objects.get(RPVS=RPVS)
                    try:
                        CartProduct.objects.get(Variety=var)
                        messages.error(request, "محصول مورد نظر در سبد خرید موجود است")
                    except:
                        item = CartProduct()
                        item.status = CartProductChoice.ExchangeProccess
                        item.Variety = var
                        item.Cart = CR
                        item.Fee = var.FinalPrice
                        item.Quantity = Quantity
                        Price = int(var.FinalPrice * Quantity)
                        item.Offless = var.Variety.Product.BasePrice
                        item.Amount = Price * (109 / 100)
                        if var.OffPrice > 0:
                            item.discount = var.OffPrice
                        item.save()
                        NewPRo(item)
                        Diff = math.ceil(int(item.Amount) - int(O_CP.Amount))
                        ex = Exchange()
                        ex.CP = O_CP
                        ex.NewCP = item
                        O_CP.status = CartProductChoice.ExchangeProccess
                        WareHouseReport = f"""همکار گرامی 
سفارش شماره {CR.RC} در حالت درخواست تعویض قرار گرفته است.
تا تغییر وضعیت مجدد سفارش را پردازش نکنید!
درصورتی که سفارش پردازش و ارسال شده است کارشناسان سایت را مطلع کنید """
                        if Diff > 50000:
                            Link = ""
                            Text = f"""
                                {User.Name} عزیز 
                                ما به تفاوت سفارش تعویض شده ی شما مبلغ {Diff} می باشد که از طریق لینک زیر قادر به پرداخت می باشید.
                                **توجه داشته باشید که تا زمانی که پرداخت انجام نشود سفارش شما پردازش و ارسال نخواهد شد
                                و در صورت درخواست لغو تعویض از طریق تماس با پشتیبانی درخواست خود راثبت کنید

                                لینک پرداخت: {Link}
                                
                            """
                            report = (
                                f"مبلغ {Diff} مابه التفاوت محصول تعویض شده با محصول قبلی است.سفارش بعد از پرداخت کاربر پردازش خواهد شد.",
                            )

                            messages.warning(request, report)
                        elif Diff < 0:
                            Diff = abs(Diff)
                            Link = ""
                            Text = f"""
                                {User.Name} عزیز 
                                ما به تفاوت سفارش تعویض شده ی شما مبلغ {Diff} می باشد که از طریق لینک زیر قادر به ثبت اطلاعات حساب بانکی خود خواهید بود
                                **توجه داشته باشید 
                                شماره کارت / حساب جهت واریز مبلغ باید با اطلاعات هویتی ثبت شده شما در پنل کاربری مطابقت داشته باشد

                                لینک : {Link}
                                
                            """
                            report = (
                                f"مبلغ {Diff} مابه التفاوت محصول تعویض شده با محصول قبلی است.مبلغ ذکر شده بعد از وارد کردن اطلاعات بانکی توسط کاربر به حساب خریدار واریز می شود",
                            )
                            messages.warning(request, report)
                        else:
                            report = "ما به التفاوت تعویض محصولات صفر می باشد و سفارش در وضعیت پردازش مجدد قرار دارد"
                            if Diff < 50000 and Diff > 0:
                                report = f"مبلغ {Diff} ریال مابه التفاوت محصول تعویض شده با محصول قبلی است. مبلغ ذکر شده کمتر از 50000 ریال می باشد و کاربر نیازی به پرداخت واریز وجه نخواهد داشت.سفارش در مرحله ی پردازش قرار گرفته است."
                                messages.warning(request, report)
                                AccountantReport = f"""همکار گرامی 
                                محصولاتی از سفارش شماره {CR.RC} تعویض شده اند.
                                ما به التفاوت اقلام تعویض شده کمتر از 50000 ریال بوده و به صورت خودکار صفر شده است

                                """
                                WST = Staff.objects.get(Position="4")
                                SendSMS(WST.Phone, AccountantReport)
                            WareHouseReport = f"""همکار گرامی 
سفارش شماره {CR.RC} شامل تغییرات شده است!
سفارش را مجددا پردازش کنید.
درصورتی که سفارش پردازش و ارسال شده است کارشناسان سایت را مطلع کنید 
                            """
                            Text = f"""
                            {User.Name} عزیز 
                            تعویض سفارش شما با موفقیت انجام شد
                            و پس از پردازش مجدد ارسال خواهد شد
                            سپاس از خرید شما
                            
                            """
                            O_CP.status = CartProductChoice.Exchanged
                        ex.Report = report
                        ex.save()
                        O_CP.save()
                        CR.status = CartChoice.ExchangeRequest
                        CR.save()
                        ST = Staff.objects.get(Position="3")
                        SendSMS(ST.Phone, WareHouseReport)
                        SendSMS(User.Phone, Text)
                    return redirect(request.META["HTTP_REFERER"])
        return render(request, self.change_form_template, context)

    def get_urls(self):
        urls = super().get_urls()
        custom_url = [
            path("cart-data/", self.admin_site.admin_view(self.add_view), name="cart-data"),
        ]
        return custom_url + urls


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("User",)
    list_filter = ("User",)
    ordering = ("Created",)
