from django.contrib import admin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from .models import (
    ContactUs,
    Slider,
    TwinBox,
    BigSellBox,
    DiscountBox,
    OfferBox,
    MiniBox,
    Shortener,
    CodeReg,
    QuickOffer,
    Staff,
)

# Register your models here.

# admin.site.register(CodeReg)
admin.site.register(Shortener)
admin.site.register(TwinBox)
admin.site.register(BigSellBox)
admin.site.register(MiniBox)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("Name", "Phone", "Position")
    list_filter = ("Gender",)
    search_fields = (
        "Name",
        "Phone",
    )
    ordering = ("Name",)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("Type",)
    readonly_fields = ("RS",)
    ordering = ("-Created",)


@admin.register(QuickOffer)
class QuickOfferAdmin(admin.ModelAdmin):
    list_display = [
        "Name",
        "Image",
        "Url",
    ]
    readonly_fields = [
        "Name",
        "Image",
        "Url",
    ]
    search_fields = ("Name",)
    ordering = ("Created",)


@admin.register(OfferBox)
class OfferBoxAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = (
        "Variety",
        "Time",
    )


@admin.register(DiscountBox)
class DiscountBoxAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = (
        "Variety",
        "Time",
    )


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("Name", "Phone", "Subject")
    ordering = ("Created",)
