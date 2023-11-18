from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
from Main.serializers import PhoneCodeRegSerializer
from Main.views import Code
from rest_framework import status
from Users.models import UserInfo
from Users.serializers import UserLoginSerializer, UserPhoneSerializer, UserRegisterSerializer
from django.core import serializers
from django.core.mail import send_mail
from Warehouse.models import Cart, CartProduct, WishList, CartChoice
import rsa
from django.core.cache import cache
from core.settings import (
    pbKEYn,
    pbKEYe,
    prKEYd,
    prKEYp,
    prKEYq,
)


def redirectView(request):
    return redirect("/")


def logoutView(request):
    cache.clear()
    del request.session["User_id"]
    return redirect("MainIndex")


class UserSignInUp(TemplateView):
    template_name = "Users/UserRegister.html"

    def get(self, request, *args, **kwargs):
        if "User_id" in request.session:
            return redirect("/")
        return super().get(request, *args, **kwargs)


class UserPhoneRegister(APIView):
    def post(self, request, *args, **kwargs):
        stat = 500
        try:
            stat = 200
            try:
                UserInfo.objects.get(Phone=request.data["Phone"])
                try:
                    way = request.data["LoginCode"]
                    if way:
                        stat = 200
                        Code(request, request.data["Phone"], "Phone")
                except:
                    stat = 302
                context = {"report": request.data, "stat": stat}
                return Response(context, status=status.HTTP_200_OK)
            except:
                res = Code(request, request.data["Phone"], "Phone")
                context = {"report": request.data, "stat": stat}
                return Response(context, status=status.HTTP_200_OK)
        except:
            stat = 500
            report = "مشکلی پیش آمده است!"
            context = {"report": report, "stat": stat}
            return Response(context)


class UserCodeCheck(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PhoneCodeRegSerializer(data=request.data)
        stat = 500
        report = "اطلاعات ارسال شده صحیح نیست"
        if serializer.is_valid():
            stat = 200
            try:
                user = UserInfo.objects.get(Phone=request.data["Phone"])
                request.session["User_id"] = user.slug
                stat = 300
                context = {"report": report, "stat": stat}
                return Response(context, status=status.HTTP_200_OK)
            except:
                pass
        context = {"report": report, "stat": stat}
        return Response(context)


class Register(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        stat = 500
        if serializer.is_valid():
            obj = serializer.save()
            publicKey = rsa.PublicKey(pbKEYn, pbKEYe)
            obj.Password = rsa.encrypt(
                serializer.validated_data["Password"].encode("utf8"), publicKey
            )
            obj.key = rsa.encrypt(serializer.validated_data["Password"].encode("utf8"), publicKey)
            obj.save()
            stat = 200
        report = ""
        for item in serializer.errors.items():
            report += item[1][0] + "<br/>"
        context = {"report": report, "stat": stat}
        return Response(context, status=status.HTTP_200_OK)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        stat = 500
        if request.data["Type"] == "Pass":
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = UserInfo.objects.get(Phone=request.data["Phone"])
                request.session["User_id"] = user.slug
                cache.clear()
                stat = 200
                report = ""
            else:
                report = "نام کاربری یا رمز عبور اشتباه است"
        elif request.data["Type"] == "Phone":
            try:
                phone = request.data["Phone"]
                UserInfo.objects.get(Phone=phone)
                Code(request, phone, "Phone")
                stat = 200
                report = ""

            except:
                report = "حساب کاربری با شماره وارد شده ثبت نشده است"
        elif request.data["Type"] == "Code":
            serializer = PhoneCodeRegSerializer(data=request.data)
            if serializer.is_valid():
                user = UserInfo.objects.get(Phone=request.data["Phone"])
                request.session["User_id"] = user.slug
                stat = 200
                report = ""
            else:
                report = "کد وارد شده صحیح نیست"
        context = {"report": report, "stat": stat}
        return Response(context, status=status.HTTP_200_OK)


class Panel(TemplateView):
    template_name = "Users/panel.html"

    def get(self, request, *args, **kwargs):
        if "User_id" not in request.session:
            return redirect("user_sign")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.request.session["User_id"]
        user = UserInfo.objects.get(slug=slug)
        Cr = Cart.objects.filter(User=user, Active=True)

        context["user"] = user
        context["Cart"] = Cr
        return context


class ChangePhoneCode(APIView):
    def post(self, request, *args, **kwargs):
        # TODO SMS
        try:
            UserInfo.objects.get(Phone=request.data["Phone"])
            report = "کاربر دیگری با این تلفن همراه ثبت شده است"
            stat = 500
        except:
            stat = 200
            Code(request, request.data["Phone"], "Phone")
            report = ""
        context = {"report": report, "stat": stat}
        return Response(context)


class ChangePhone(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PhoneCodeRegSerializer(data=request.data)
        stat = 500
        report = "اطلاعات ارسال شده صحیح نیست"
        if serializer.is_valid():
            stat = 200
            try:
                slug = request.session["User_id"]
                user = UserInfo.objects.get(slug=slug)
                user.Phone = request.data["Phone"]
                user.save()
                stat = 200
                context = {"report": report, "stat": stat}
                return Response(context, status=status.HTTP_200_OK)
            except:
                pass
        context = {"report": report, "stat": stat}
        return Response(context)


class getUserData(APIView):
    def get(self, request, *args, **kwargs):
        slug = request.session["User_id"]
        user = UserInfo.objects.get(slug=slug).toJson()
        return Response(user)
