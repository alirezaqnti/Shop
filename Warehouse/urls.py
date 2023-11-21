from django.urls import path
from . import views

urlpatterns = [
    path("addtocart/", views.AddToCart.as_view(), name="addtocart"),
    path("removefromcart/", views.RemoveFromCart.as_view(), name="removefromcart"),
    path("removecart/", views.RemoveCart.as_view(), name="RemoveCart"),
    path("refresh-cart/", views.RefreshCart.as_view(), name="RefreshCart"),
    path("getcart/", views.GetCart.as_view(), name="getcart"),
    path("cartcheck/", views.CartCheck.as_view(), name="CartCheck"),
    path("addtowishlist/", views.AddToWishlist.as_view(), name="addtowishlist"),
    path(
        "removefromwishlist/",
        views.RemoveFromWishlist.as_view(),
        name="removefromwishlist",
    ),
    path("getwishlist/", views.GetWishlist.as_view(), name="getwishlist"),
    path("cartpayment/", views.CartPaymentView.as_view(), name="CartPaymentView"),
    path("check-coupon/", views.CheckCoupon.as_view(), name="CheckCoupon"),
    path("fortune/getpermission/", views.GetPermission.as_view(), name="GetPermission"),
    path("fortune/set-prize/", views.SetPrize.as_view(), name="SetPrize"),
    path("unattach-coupon/", views.UnattachCoupon.as_view(), name="UnattachCoupon"),
    path("invoicereport/<str:RC>", views.InvoiceReport.as_view(), name="InvoiceReport"),
    path("payment/callback/zarinpal/", views.ZarinpalCallback, name="ZarinpalCallback"),
    path("payment/report/<str:RC>", views.PostPaymentView, name="PostPaymentView"),
    path("payment/zarintest/", views.zarintest, name="zarintest"),
]
