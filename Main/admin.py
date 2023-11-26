from django.contrib import admin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from .models import ContactUs, ImageBox, Staff, Offers

# Register your models here.


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("Name", "Phone", "Position")
    list_filter = ("Gender",)
    search_fields = (
        "Name",
        "Phone",
    )
    ordering = ("Name",)


@admin.register(ImageBox)
class ImageBoxAdmin(admin.ModelAdmin):
    list_display = (
        "RS",
        "Placement",
        "Type",
    )
    readonly_fields = ("RS",)
    ordering = ("-Created",)


@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = [
        "Product",
        "Type",
        "Sub",
    ]
    readonly_fields = [
        "Product",
    ]
    search_fields = (
        "Product.Name",
        "Product.RP",
        "Sub.RPVS",
    )
    ordering = ("Created",)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("Name", "Phone", "Subject")
    ordering = ("Created",)
