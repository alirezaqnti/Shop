from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from Warehouse.models import (
    Cart,
    CartProduct,
    WishList,
    CartChoice,
    Coupon,
    CouponUser,
    CartPayment,
    PaymentPortals,
    paymentChoice,
    WheelOfFortune,
    FortuneUser,
)
from Main.context_processors import getActiveUser, getCart
from Main.views import SendSMS
from Main.models import Staff
from Main.permissions import IsUserLoggedIn
from Products.models import Variety, Product, ProductImage, VarietySub, Category
from django.core.cache import cache
from django.db import transaction
from django.views.generic import TemplateView
from datetime import datetime
from time import sleep
from .PayemrntBackend import GetClient, MERCHANT
from core.settings import REFFERER
from django.shortcuts import redirect
import jdatetime
import logging

logger = logging.getLogger("django")


def NewPRo(obj):
    cart = obj.Cart
    cart.Amount += obj.Fee
    cart.TotalPrice += obj.Amount
    cart.TotalDiscount += obj.discount
    cart.weight += obj.weight
    cart.save()
    return True


class AddToCart(IsUserLoggedIn, APIView):
    def post(self, request, *args, **kwargs):
        try:
            kw = kwargs["kwargs"]
            RPVS = kw["RPVS"]
            Quan = kw["Quantity"]
        except:
            RPVS = False
            Quan = 1
        RPVS = request.data.get("RPVS", RPVS)
        Quantity = int(request.data.get("Quantity", Quan))
        stat = 500
        if not RPVS:
            stat = 500
        else:
            with transaction.atomic():
                var = VarietySub.objects.get(RPVS=RPVS)
                user = getActiveUser(request)
                if user == "":
                    stat = 301
                else:
                    try:
                        cr = Cart.objects.get(
                            User=user, status=CartChoice.Created, Active=True
                        )
                    except:
                        cr = Cart.objects.create(User=user)
                    try:
                        item = CartProduct.objects.get(Cart=cr, Variety=var)
                        if item.Quantity == Quantity:
                            stat = 202
                        else:
                            item.Quantity = Quantity
                            item.save()
                    except:
                        item = CartProduct()
                        item.Variety = var
                        item.Cart = cr
                        item.Fee = var.FinalPrice
                        item.Quantity = Quantity
                        Price = var.FinalPrice * Quantity
                        item.Offless = var.Variety.Product.BasePrice
                        item.Amount = Price
                        if var.OffPrice > 0:
                            item.discount = var.OffPrice
                        item.save()
                        NewPRo(item)
                        cache.delete("cart")
                stat = 200

        context = {"stat": stat}
        return Response(context)


class RemoveCart(APIView):
    def post(self, request, *args, **kwargs):
        cart = getCart(request)
        cr = Cart.objects.get(RC=cart["RC"])
        cr.delete()
        context = getCart(request)
        return Response(context)


class RefreshCart(APIView):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        cart = getCart(request)
        try:
            kw = kwargs["kwargs"]
        except:
            kw = False
        RCPs = request.data.get("RCPs", kw)
        print("RCPs:", RCPs)
        for item in RCPs:
            print(item)
            CP = CartProduct.objects.get(RCP=item)
            cart = CP.Cart
            stat = 304
            try:
                cr = CartProduct.objects.filter(Cart=cart)
                if cr.count() <= 1:
                    cart.delete()
                else:
                    CP.delete()

            except:
                stat = 500
        cache.delete("cart")
        context = {
            "stat": stat,
        }
        return Response(context)


class ChangeCartProduct(APIView):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        RCP = request.data["RCP"]
        Quantity = int(request.data["Quantity"])
        print("RCP:", RCP)
        print("Quantity:", Quantity)
        stat = 500
        report = ""
        try:
            CP = CartProduct.objects.get(RCP=RCP)
            CR = CP.Cart
            Var = CP.Variety
            if Var.Quantity > Quantity:
                CP.delete()
                item = CartProduct()
                item.Variety = Var
                item.Cart = CR
                item.Fee = Var.FinalPrice
                item.Quantity = Quantity
                Price = Var.FinalPrice * Quantity
                item.Offless = Var.Variety.Product.BasePrice
                item.Amount = Price
                if Var.OffPrice > 0:
                    item.discount = Var.OffPrice
                item.save()
                NewPRo(item)
                cache.delete("cart")
                stat = 200
            else:
                stat = 500
                report = "موجودی محصول کافی نیست!"
        except:
            stat = 500
            report = "مشکلی پیش آمده است، لطفا بعدا تلاش کنید!"
        return Response({"stat": stat, "report": report})


class RemoveFromCart(APIView):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        user = getActiveUser(request)
        cart = getCart(request)
        try:
            kw = kwargs["kwargs"]
        except:
            kw = False
        RCP = request.POST.get("RCP", kw)
        var = CartProduct.objects.get(RCP=RCP)
        cart = var.Cart
        stat = 304
        data = {"RCP": RCP}
        if user == "":
            stat = 301
        else:
            try:
                cr = CartProduct.objects.filter(Cart=cart)
                if cr.count() <= 1:
                    cart.delete()
                else:
                    var.delete()

            except:
                stat = 500
        cache.delete("cart")
        context = {
            "stat": stat,
            "data": data,
        }
        return Response(context)


class GetCart(APIView):
    def post(self, request, *args, **kwargs):
        try:
            cache.delete("cart")
        except:
            pass
        context = getCart(request)
        RC = context["RC"]
        cr = Cart.objects.filter(RC=RC).prefetch_related("shipping_cart")
        try:
            Ship = cr.shipping_cart
            if Ship.Type == "0":
                Type = "پیک موتوری"
            else:
                Type = "پست"
            Address = f"{Ship.State.title}، {Ship.City.title}، {Ship.Address} ، پلاک {Ship.No}، واحد {Ship.Unit}"
            context["Address"] = Address
        except:
            pass
        return Response(context)


class AddToWishlist(APIView):
    def post(self, request, *args, **kwargs):
        user = getActiveUser(request)
        if user != "":
            RPVS = request.POST.get("RPVS")
            var = VarietySub.objects.get(RPVS=RPVS)
            stat = 200
            try:
                wh = WishList.objects.get(User=user, Variety=var)
                stat = 202
            except:
                wh = WishList.objects.create(User=user, Variety=var)
        else:
            stat = 301
        context = {"stat": stat}
        return Response(context)


class RemoveFromWishlist(APIView):
    def post(self, request, *args, **kwargs):
        RW = request.POST.get("RW")
        WishList.objects.get(RW=RW).delete()
        stat = 305
        context = {"stat": stat}
        return Response(context)


class GetWishlist(APIView):
    def get(self, request, *args, **kwargs):
        user = getActiveUser(request)
        wh = WishList.objects.filter(User=user)
        data = []
        for item in wh:
            pic = ProductImage.objects.get(
                Product=item.Variety.Variety.Product, Primary=True
            )
            dic = {
                "Name": item.Variety.Variety.Product.Name,
                "Pic": str(pic.Image),
                "Size": item.Variety.Size,
                "Color": item.Variety.Variety.ColorCode,
                "RW": item.RW,
            }
            data.append(dic)

        context = {
            "count": wh.count(),
            "Pros": data,
        }
        return Response(context)


def zarintest(request):
    CallbackURL = f"{REFFERER}warehouse/payment/callback/zarinpal/"
    email = "sdfzgdx@gmail.com"
    mobile = "09177831766"
    description = "پرداخت نوبت"
    client = GetClient()
    logger.info("Cilent:", client)
    result = client.service.PaymentRequest(
        MERCHANT, 5000, description, email, mobile, CallbackURL
    )
    logger.info("RES:", result)
    if result.Status == 100:
        stat = 200
        url = f"https://www.zarinpal.com/pg/StartPay/{str(result.Authority)}"
        context = {"stat": stat, "url": url}
        return redirect(url)
    else:
        return HttpResponse("Failed!")


class CartPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        data = cache.get("PaymentData")
        RC = data["RC"]
        PW = data["Way"]
        Cr = (
            Cart.objects.filter(RC=RC)
            .prefetch_related("cartproduct_cart", "shipping_cart")
            .first()
        )
        with transaction.atomic():
            for item in Cr.cartproduct_cart.filter(Active=True):
                Var = item.Variety
                if Var.Quantity <= item.Quantity:
                    Var.ReserevedQuantity += item.Quantity
                    Var.Quantity -= item.Quantity
                    Var.save()
                else:
                    context = {"stat": 200}
                    return Response(context)
            if PW == "zarinpal":
                CallbackURL = f"{REFFERER}warehouse/payment/callback/zarinpal/"
                email = ""
                mobile = ""
                description = "پرداخت نوبت"
                client = GetClient()
                Amount = Cr.TotalPrice / 10
                result = client.service.PaymentRequest(
                    MERCHANT, Amount, description, email, mobile, CallbackURL
                )
                if result.Status == 100:
                    try:
                        Cr = CartPayment.objects.get(
                            Cart=Cr,
                            Amount=Amount,
                        )
                        Cr.Portal = PaymentPortals.zarinpal
                        Cr.Auth = result.Authority
                        Cr.save()
                    except:
                        CartPayment.objects.create(
                            Auth=result.Authority,
                            Cart=Cr,
                            Amount=Amount,
                            Portal=PaymentPortals.zarinpal,
                        )
                    stat = 200
                    url = (
                        f"https://www.zarinpal.com/pg/StartPay/{str(result.Authority)}"
                    )
                    context = {"stat": stat, "url": url}
                    return redirect(url)
                else:
                    return redirect("PostPaymentView", Cr.RC)
        context = {"stat": 200}
        return Response(context)


def ZarinpalCallback(request):
    pay = CartPayment.objects.get(Auth=request.GET["Authority"])
    Cr = (
        Cart.objects.filter(pk=pay.Cart_id)
        .prefetch_related("cartproduct_cart", "shipping_cart")
        .first()
    )
    Ord = Cr.cartproduct_cart.filter(Active=True)
    with transaction.atomic():
        if request.GET.get("Status") == "OK":
            client = GetClient()
            result = client.service.PaymentVerification(
                MERCHANT, request.GET["Authority"], pay.Amount
            )
            if result.Status == 100:
                refId = str(result.RefID)
                # TODO May need to get sessions again
                refId = str(result.RefID)
                pay.Ref = refId
                pay.Status = result.Status
                pay.save()
                Cr.PurchaseTrackNumber = refId
                Cr.PaymentDate = jdatetime.datetime.today().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                Cr.PaymentWay = paymentChoice.Zarinpal
                Cr.status = CartChoice.InProccess
                Cr.policyAccept = True
                Cr.save()
                for item in Ord:
                    proUser = item.Variety
                    proUser.ReserevedQuantity -= item.Quantity
                    proUser.save()  # ذخیره محصول
                User = Cr.User
                text = f"""
{User.Name} عزیز
سفارش شماره {Cr.RC} ثبت شد و در حال پردازش است
سپاس از خرید شما
www.mohsenvafaienejad.com
"""
                SendSMS(Cr.User.Phone, text)
                St = Staff.objects.get(Position="3")
                text = f"""
همکار عزیز
سفارش جدیدی ثبت شده است
از طریق لینک زیر اقدام به مشاهده و پردازش سفارش کنید

لینک :
{REFFERER}warehouse/invoicereport/{Cr.RC}

                """
                SendSMS(St.Phone, text)
                return redirect("PostPaymentView", Cr.RC)
            elif result.Status == 101:
                refId = str(result.RefID)
                Cr.PurchaseTrackNumber = refId
                Cr.save()
                return redirect("PostPaymentView", Cr.RC)
            elif result.Status == -51:
                return redirect("PostPaymentView", Cr.RC)
        else:
            pay.Status = request.GET.get("Status")
            pay.save()
            for item in Ord:
                proUser = item.Variety
                proUser.ReserevedQuantity -= item.Quantity
                proUser.Quantity += item.Quantity
                proUser.save()  # ذخیره محصول
            return redirect("PostPaymentView", Cr.RC)


def PostPaymentView(request, RC):
    Cr = (
        Cart.objects.filter(RC=RC)
        .prefetch_related("cartproduct_cart", "shipping_cart")
        .first()
    )
    Pay = CartPayment.objects.get(Cart=Cr)
    if Pay.Status in ["100", "101"]:
        return render(request, "Main/PaymentSuccess.html", {"Cart": Cr, "Payment": Pay})
    else:
        return render(request, "Main/PaymentFailed.html", {"Cart": Cr, "Payment": Pay})
    # try:
    # except:
    #     # TODO Handle 404
    #     pass


class InvoiceReport(TemplateView):
    template_name = "Warehouse/Invoice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        RC = self.kwargs["RC"]
        Cr = (
            Cart.objects.filter(RC=RC)
            .prefetch_related("cartproduct_cart", "shipping_cart")
            .first()
        )
        context["Cart"] = Cr
        return context


class CheckCoupon(APIView):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        Check = False
        Code = request.data["Code"]
        RC = request.data["RC"]
        User = getActiveUser(request)
        try:
            Cou = Coupon.objects.get(Code=Code)
            date = datetime.now()
            Time = Cou.Time.replace(tzinfo=None)
            if date <= Time:
                try:
                    Couser = CouponUser.objects.get(User=User, Coupon=Cou)
                    if Couser.Usage >= Cou.MaxUse:
                        return Response(
                            {"Check": False, "Mess": "قبلا استفاده شده است"}
                        )
                    else:
                        Couser.Usage += 1
                        Couser.save()
                except:
                    Couser = CouponUser()
                    Couser.Coupon = Cou
                    Couser.User = User
                    Couser.Usage = 1
                    Couser.save()
                Check = True
                Mess = "کد تخفیف با موفقیت اعمال شد"
            else:
                Mess = "کوپن مورد نظر منقضی شده است"
        except:
            Mess = "کد وارد شده صحیح نمی باشد"

        if Check:
            Cr = Cart.objects.filter(RC=RC).prefetch_related("cartproduct_cart").first()
            if Cou.Type == "1":
                Prs = Product.objects.filter(
                    Category__in=Category.objects.get(
                        pk=Cou.Category.pk
                    ).get_descendants(include_self=True)
                )
                CPs = Cr.cartproduct_cart.all()
                for item in CPs:
                    if item.Variety.Variety.Product in Prs:
                        Cr.TotalPrice -= item.Amount
                        Cr.Amount -= item.Fee
                        Cr.TotalDiscount -= item.discount
                        Price = item.Offless * ((100 - Cou.Discount) / 100)
                        Discount = item.Offless * (Cou.Discount / 100)
                        if Discount > Cou.MaxPrice:
                            Price = item.Offless - Cou.MaxPrice
                        Amount = Price * item.Quantity
                        item.Amount = Amount
                        item.discount = Discount
                        item.Vouchered = True
                        item.save()
                        Cr.TotalPrice += Amount
                        Cr.Amount += Amount
                        Cr.TotalDiscount += Discount
                        Cr.save()
            elif Cou.Type == "2":
                Cr.TotalPrice -= Cr.Amount
                if Cou.Discount != 0:
                    Price = Cr.Amount * ((100 - Cou.Discount) / 100)
                    Discount = Cr.Amount * (Cou.Discount / 100)
                    print("Discount:", Discount)
                    print("MaxPrice:", Cou.MaxPrice)
                    print("COMPARE:", Discount > Cou.MaxPrice)
                    if Discount > Cou.MaxPrice:
                        Price = Cr.Amount - Cou.MaxPrice
                        Discount = Cou.MaxPrice
                else:
                    Price = Cr.Amount - Cou.MaxPrice
                    Discount = Cou.MaxPrice
                Cr.TotalPrice += Price
                Cr.Amount = Price
                Cr.TotalDiscount += Discount
                Cr.save()
                Couser.Amount = Discount
                Couser.save()
            Cr.Vouchered = True
            Cr.VoucherCode = Code
            Cr.save()

        return Response({"Check": Check, "Mess": Mess})


class UnattachCoupon(APIView):
    def post(self, request, *args, **kwargs):
        RC = request.data["RC"]
        User = getActiveUser(request)
        Cr = Cart.objects.filter(RC=RC).prefetch_related("cartproduct_cart").first()
        Cou = Coupon.objects.get(Code=Cr.VoucherCode)
        Couser = CouponUser.objects.get(User=User, Coupon=Cou)
        Check = False
        if Cou.Type == "1":
            CPs = Cr.cartproduct_cart.filter(Vouchered=True)
            for item in CPs:
                RPVS = item.Variety.RPVS
                Quantity = item.Quantity
                kw = {
                    "RPVS": RPVS,
                    "Quantity": Quantity,
                }
                RemoveFromCart.post(self, request=request, kwargs=item.RCP)
                sleep(2)
                AddToCart.post(
                    self, request=request, kwargs={"RPVS": RPVS, "Quantity": Quantity}
                )
            Check = True
            Mess = "کوپن با موفقیت حذف شد"
        elif Cou.Type == "2":
            Price = Couser.Amount
            Cr.TotalPrice += Price
            Cr.Amount += Price
            Cr.TotalDiscount -= Price
            Cr.save()
            Couser.Amount = 0
            Couser.save()
            Cr.Vouchered = False
            Cr.VoucherCode = ""
            Cr.save()
            Check = True
            Mess = "کوپن با موفقیت حذف شد"

        if Check:
            if Couser.Usage > 1:
                Couser.Usage -= 1
                Couser.save()
            else:
                Couser.delete()
        return Response({"Check": Check, "Mess": Mess})


class SetPrize(APIView):
    def post(self, request, *args, **kwargs):
        user = getActiveUser(request)
        stat = 500
        if user != "":
            WH = (
                WheelOfFortune.objects.filter(Active=True)
                .prefetch_related("user_wheel", "prize_wheel")
                .first()
            )
            PR = WH.prize_wheel.filter(RFP=request.data["RFP"]).first()
            user_ = WH.user_wheel.filter(User=user)
            text = f"""
            {user.Name} عزیز
            شما برنده ی "{PR.Title}" در گردونه ی شانس شدید
            با استفاده از کد {PR.Coupon.Code} در سبد خرید خود می توانید از جایزه ی خود استفاده کنید
            """
            if user_.count() != 0:
                FU = user_.first()
                if FU.Usage >= WH.MaxUse:
                    stat = 300
                else:
                    SendSMS(user.Phone, text)
                    FU.Usage += 1
                    FU.save()
                    stat = 200
            else:
                FU = FortuneUser()
                FU.Wheel = WH
                FU.User = user
                FU.Usage = 1
                FU.Prize = PR
                FU.save()
                SendSMS(user.Phone, text)
                stat = 200
        return Response({"stat": stat})


class GetPermission(APIView):
    def get(self, request, *args, **kwargs):
        user = getActiveUser(request)
        if user != "":
            WH = (
                WheelOfFortune.objects.filter(Active=True)
                .prefetch_related("user_wheel")
                .first()
            )
            user_ = WH.user_wheel.filter(User=user).count()
            if user_ == 0:
                stat = 200
            else:
                stat = 300
        else:
            stat = 500
        return Response({"stat": stat})


class CartCheck(IsUserLoggedIn, APIView):
    def post(self, request, *args, **kwargs):
        user = getActiveUser(request)
        CR = (
            Cart.objects.filter(User=user, Active=True, status=CartChoice.Created)
            .prefetch_related("cartproduct_cart")
            .first()
        )
        CPs = CR.cartproduct_cart.all()
        res = []
        for item in CPs:
            if item.Quantity > item.Variety.Quantity:
                res.append(item.RCP)

        return Response({"CPs": res})
