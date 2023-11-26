from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.HomepageView.as_view(), name="MainIndex"),
    path("contact-us/", views.ContactView.as_view(), name="ContactView"),
    path(
        "purchase-track/",
        views.PurchaseTrackingView.as_view(),
        name="PurchaseTrackingView",
    ),
    path("about-us/", views.AboutView.as_view(), name="AboutView"),
    path("cart/", views.CartView.as_view(), name="CartView"),
    path("checkout/", views.CheckoutView.as_view(), name="CheckoutView"),
    path("csrf/", views.get_csrf),
    path("getcity/", views.GetCity.as_view()),
    path("urlsession/", views.URLSession),
    path("retriveurlsession/", views.RetriveURLSession),
    path("wheel-of-fortune/", views.WheelView.as_view(), name="WheelView"),
    path("getwheeldata/", views.GetWheelData.as_view(), name="GetWheelData"),
    path("slide/<str:RS>", views.ImageBoxDataView.as_view(), name="ImageBoxDataView"),
]
