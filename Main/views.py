import random
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView
from rest_framework.response import Response
from Users.models import UserInfo
from Blog.models import Post
from .models import CodeReg, ImageBox, ContactUs, City, Staff, Offers
from .forms import ContactForm
from kavenegar import KavenegarAPI
from django.middleware.csrf import get_token
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.core.mail import send_mail

from Main.context_processors import getActiveUser, getCart
from Main.serializers import OfferSerializer
from Main.models import Address
from Products.serializers import ProductSerializer
from Products.models import (
    ProductImage,
    CategoryToPreview,
    BrandToPreview,
    Testimotional,
)
from Warehouse.models import (
    Cart,
    CartProduct,
    Shipping,
    CartChoice,
    WheelOfFortune,
    PurchaseTrack,
)
from django.contrib import messages
import requests
from django.db import transaction
from Warehouse.serializers import WheelSerializer
from kavenegar import KavenegarAPI

try:
    from core.Private import KAVENEGAR_API_KEY
except:
    KAVENEGAR_API_KEY = ""
# def html_email():
#     subject = 'That’s your subject'
#     html_message = render_to_string('mail_template.html', {'context': 'values'})
#     plain_message = strip_tags(html_message)
#     from_email = 'from@yourdjangoapp.com>'
#     to = 'to@yourbestuser.com'
#     mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def get_csrf(request):
    response = JsonResponse({"Info": "Success - Set CSRF cookie"})
    response["X-CSRFToken"] = get_token(request)
    return response


# region Send SMS
# send a single token sms
def SendSMS(data):
    try:
        api = KavenegarAPI(KAVENEGAR_API_KEY)
        params = {
            "receptor": data["Phone"],
            "template": data["template"],
        }
        try:
            params["token"] = data["token"]
        except:
            pass

        try:
            params["token2"] = data["token2"]
        except:
            pass

        try:
            params["token3"] = data["token3"]
        except:
            pass

        try:
            params["token10"] = data["token10"]
        except:
            pass
        try:
            params["token20"] = data["token20"]
        except:
            pass

        response = api.verify_lookup(params)
    except Exception as e:
        print(e)


# endregion

# region Code
# functions:
# ایجاد یک کد ۶ رقمی برای اعتبار سنجی تلفن همراه
# ورودی ها:
# شماره تلفن همراه
# خروجی :
# کد ۶ رقمی


def Code(phone):
    co = CodeReg()
    co.Phone = phone
    co.save()
    number = co.Code
    template = "LomerUserPhoneNOVerification"
    data = {
        "template": template,
        "token": number,
        "Phone": phone,
    }
    SendSMS(data)
    # if request.POST and request.is_ajax():
    #     number = random.randint(100000, 999999)
    #     request.session["code"] = number
    #     stat = 200
    #     return JsonResponse({"stat": stat})
    return number


# endregion


def URLSession(request):
    if request.POST:
        url = request.POST["URL"]
        request.session["URL"] = url
        return JsonResponse({"stat": 200})


def RetriveURLSession(request):
    if "URL" in request.session:
        url = request.session["URL"]
    else:
        url = request.headers["Host"]
    return JsonResponse({"URL": url})


class GetCity(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data["id"]
        cities = City.objects.filter(parent=id).reverse()
        data = []
        for i in cities:
            data.append({"id": i.id, "title": i.title})
        context = {"data": data}
        return JsonResponse(context)


class HomepageView(TemplateView):
    template_name = "Main/home.html"

    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        IMs = ImageBox.objects.filter(Active=True).order_by("-Order")
        SB = IMs.filter(Placement="1")
        BB = IMs.filter(Placement="2").first()
        TB = IMs.filter(Placement="3")
        CP = CategoryToPreview.objects.filter(Active=True)[:7]
        BR = BrandToPreview.objects.filter(Active=True)[:7]
        TS = Testimotional.objects.filter(Active=True)[:7]
        Lt = Post.objects.filter(Active=True).order_by("-Created_At")[:5]
        context["Posts"] = Lt
        context["Slides"] = SB
        context["BigBox"] = BB
        context["TripleBox"] = TB
        context["CategoryToPreview"] = CP
        context["BrandToPreview"] = BR
        context["Testimotional"] = TS
        return context


class CartView(TemplateView):
    template_name = "Main/cart.html"


class CheckoutView(TemplateView):
    template_name = "Main/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = getActiveUser(self.request)
        cities = City.objects.filter(parent=0)
        cart = getCart(self.request)
        context["Cart"] = cart
        context["Pros"] = cart["Pros"]
        context["City"] = cities
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        RC = request.POST["RC"]
        Cr = (
            Cart.objects.filter(RC=RC)
            .prefetch_related("cartproduct_cart", "shipping_cart")
            .first()
        )
        Name = request.POST.get("Name", False)
        Phone = request.POST.get("Phone", False)
        State = request.POST.get("State", False)
        City = request.POST.get("City", False)
        No = request.POST.get("No", False)
        Unit = request.POST.get("Unit", False)
        PostCode = request.POST.get("PostCode", False)
        PostalAddress = request.POST.get("PostalAddress", False)
        Tips = request.POST.get("Tips", False)
        PaymentWay = request.POST.get("PaymentWay", False)
        ShippingWay = request.POST.get("ShippingWay", False)
        SaveAddress = request.POST.get("SaveAddress", False)
        print("SaveAddress:", SaveAddress)
        try:
            Cr.shipping_cart.delete()
        except:
            pass
        Ship = Shipping()
        Ship.Cart = Cr
        Ship.Name = Name
        Ship.Phone = Phone
        Ship.State_id = State
        Ship.City_id = City
        Ship.PostalAddress = PostalAddress
        Ship.PostalCode = PostCode
        Ship.No = No
        if Unit:
            Ship.Unit = Unit
        if Tips:
            Ship.Tips = Tips
        if ShippingWay == "post":
            Ship.Type = 1
            ShippingPrice = 600000
        else:
            Ship.Type = 0
            ShippingPrice = 150000
        Ship.save()
        if SaveAddress == "on":
            Add = Address()
            Add.User = Cr.User
            Add.Name = Name
            Add.Phone = Phone
            Add.State_id = State
            Add.City_id = City
            Add.PostalAddress = PostalAddress
            Add.PostalCode = PostCode
            Add.Number = No
            Add.Unit = Unit
            Add.save()
        Cr.PaymentWay = 1 if PaymentWay == "bank" else 2
        Cr.policyAccept = True
        if Cr.ShippingPriceAdded:
            Cr.TotalPrice -= Cr.ShippingPrice
        Cr.ShippingPrice = ShippingPrice
        Cr.TotalPrice += ShippingPrice
        Cr.ShippingPriceAdded = True
        Cr.save()
        data = {}
        data["RC"] = Cr.RC
        data["Way"] = PaymentWay
        cache.set("PaymentData", data)
        return redirect("CartPaymentView")


class AboutView(TemplateView):
    template_name = "Main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        BR = BrandToPreview.objects.filter(Active=True)[:7]
        TS = Testimotional.objects.filter(Active=True)[:7]
        context["BrandToPreview"] = BR
        context["Testimotional"] = TS
        return context


class ContactView(FormView):
    template_name = "Main/contact.html"
    form_class = ContactForm
    success_url = "/contact-us/"

    def form_valid(self, form: form_class):
        form.save()
        messages.success(
            self.request,
            "درخواست شما با موفقیت ثبت شد! در صورت نیاز همکاران ما با شما تماس خواهند گرفت.",
        )
        return super().form_valid(form)


class WheelView(TemplateView):
    template_name = "Main/Wheel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        WH = (
            WheelOfFortune.objects.filter(Active=True)
            .prefetch_related("prize_wheel")
            .first()
        )

        context["Wheel"] = WH
        return context


class GetWheelData(ListAPIView):
    queryset = WheelOfFortune.objects.filter(Active=True).prefetch_related(
        "prize_wheel"
    )
    serializer_class = WheelSerializer


class ImageBoxDataView(TemplateView):
    template_name = "Main/Slider.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        RS = self.kwargs["RS"]
        SL = ImageBox.objects.get(RS=RS)
        context["Slide"] = SL
        return context


class PurchaseTrackingView(TemplateView):
    template_name = "Main/PurchaseTracking.html"

    def post(self, request, *args, **kwargs):
        Name = request.POST["Name"]
        Phone = request.POST["Phone"]
        CR_ = request.POST["Cart"]
        Describtion = request.POST["Describtion"]
        try:
            CR = Cart.objects.get(RC=CR_)
            PT = PurchaseTrack()
            PT.Cart = CR
            PT.User = CR.User
            PT.Phone = Phone
            PT.Describtion = Describtion
            PT.save()

            text = f"""همکار گرامی
            درخواست پیگیری سفارش ثبت شده است
            جهت پردازش درخواست به پنل ادمین مراجعه کنید

            """
            St = Staff.objects.get(Position="1")
            SendSMS(St.Phone, text)
            messages.success(
                request,
                "درخواست شما با موفقیت ثبت شد.کارشناسان ما به زودی با شما ارتباط خواهند گرفت",
            )
        except:
            messages.error(request, "سفارشی با کد وارد شده ثبت نشده است!")
        return render(request, self.template_name, self.get_context_data())
