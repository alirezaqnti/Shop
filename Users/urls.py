from django.urls import path

from . import views

urlpatterns = [
    path("", views.redirectView),
    path("logout/", views.logoutView, name="user_logout"),
    path("login/", views.Login.as_view(), name="user_login"),
    path("register/", views.UserSignInUp.as_view(), name="user_sign"),
    path("register/phone/", views.UserPhoneRegister.as_view(), name="user_phone"),
    path("register/phone/code/", views.UserCodeCheck.as_view(), name="user_code"),
    path("register/phone/code/submit/", views.Register.as_view(), name="user_register"),
    path("panel/", views.Panel.as_view(), name="user_panel"),
    path("getuserdata/", views.getUserData.as_view(), name="user_data"),
    path("phone/code/", views.ChangePhoneCode.as_view()),
    path("phone/change/", views.ChangePhone.as_view()),
]
