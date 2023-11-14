from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.core.exceptions import ValidationError
from django.http.response import HttpResponse, JsonResponse
from django.contrib import messages
from Main.models import Shortener
from core.settings import REFFERER
from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from core.settings import BASE_DIR, MEDIA_ROOT
import os
from django.db import transaction
from .models import *
from mptt.admin import MPTTModelAdmin
import random
import string
import qrcode
import jdatetime
import json


def Digits(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def Slugify(Type, Email, Phone):
    val1 = list(Email)
    val2 = list(Phone)
    res = val1 + val2
    random.shuffle(res)
    listToStr = "".join(map(str, res))
    slug = Type + "-" + listToStr
    return slug


class VarietySubInline(admin.TabularInline):
    model = VarietySub
    readonly_fields = [
        "RPVS",
        "FinalPrice",
        "OffPrice",
    ]


class FiltersInline(admin.TabularInline):
    model = Filters
    min_num = 2
    max_num = 9


class VarietyInline(admin.TabularInline):
    model = Variety
    readonly_fields = [
        "RPV",
    ]


class CommentTipInline(admin.TabularInline):
    model = CommentTip


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    """Admin View for ProductComment"""

    list_display = [
        "Product",
        "User",
        "Date",
        "Text",
        "Rate",
    ]
    list_filter = ("Date",)
    inlines = [
        CommentTipInline,
    ]
    readonly_fields = [
        "Date",
        "Text",
        "Rate",
    ]
    search_fields = ("Product",)
    ordering = ("Created_at",)


class FilterValueInline(admin.TabularInline):
    model = FilterValue


@admin.register(Filters)
class FiltersAdmin(admin.ModelAdmin):
    list_display = [
        "Name",
        "Category",
    ]
    inlines = [
        FilterValueInline,
    ]
    search_fields = ("Name",)


class ProductCommentInline(admin.TabularInline):
    """Tabular Inline View for ProductComment"""

    model = ProductComment


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    max_num = 5
    min_num = 3


class ProductTechInline(admin.TabularInline):
    model = ProductTech


class ProductForm(forms.ModelForm):
    Description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = [
            "Guarantee",
            "Category",
            "Brand",
            "Name",
            "Demo",
            "Discount",
            "BasePrice",
            "Description",
            "MetaDescription",
            "MetaTitle",
            "MetaKeywords",
        ]
        exclude = [
            "Rate",
            "RateNo",
            "Status",
            "Visit",
            "Sale",
        ]
        widgets = {
            "Demo": forms.Textarea(
                attrs={"class": "form-control", "required": "true", "rows": "4"}
            ),
            "Name": forms.TextInput(attrs={"class": "form-control", "required": "true"}),
            "Discount": forms.TextInput(attrs={"class": "form-control", "required": "false"}),
            "BasePrice": forms.TextInput(attrs={"class": "form-control", "required": "true"}),
            "MetaDescription": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "MetaTitle": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "MetaKeywords": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_Name(self):
        Name = self.cleaned_data.get("Name")
        try:
            Product.objects.get(Name=Name)
            raise forms.ValidationError("محصول دیگری با این نام ثبت شده است!")
        except:
            return Name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["RP", "Name", "Url", "Status"]
    list_filter = ["Category", "Status"]
    search_fields = [
        "RP",
        "Name",
    ]
    readonly_fields = [
        "RP",
        "Slug",
        "QrCode",
        "Url",
        "Created_at_g",
        "Modified_at_g",
        "Created_at_j",
        "Modified_at_j",
        "Visit",
        "Sale",
    ]
    inlines = [VarietyInline, ProductImageInline, ProductTechInline, ProductCommentInline]
    form = ProductForm
    add_form_template = "admin/Product.html"

    def save_model(self, request, obj, form, change):
        Type = "Product"
        if not change:
            obj.save()
            date = jdatetime.datetime.now().strftime("%Y%m%d")
            RP = f"RP-{date}{obj.pk}"
            inp = Digits()
            inpu = Digits()
            slug = Slugify(Type, inp, inpu)
            ref = request.headers["Referer"]
            name = "Qr-" + str(RP) + ".png"
            path = f"Product/{RP}/{name}"
            root = os.path.join(BASE_DIR, MEDIA_ROOT)
            root = f"{BASE_DIR}/media/Products/{RP}/{name}"
            dir = f"{BASE_DIR}/media/Products/{RP}"
            url = f"{ref}product/" + str(slug)
            qr = qrcode.make(url)
            if os.path.exists(dir):
                qr.save(root)
            else:
                os.makedirs(dir)
                qr.save(root)
            obj.QrCode = path
            obj.RP = RP
            obj.Slug = slug
            price = obj.BasePrice * ((100 - obj.Discount) / 100)
            offPrice = obj.BasePrice - price
            obj.FinalPrice = price
            obj.OffPrice = offPrice
            short = Shortener()
            short.Real = f"{REFFERER}products/{slug}"
            short.save()
            obj.Url = short.Short
        super().save_model(request, obj, form, change)

    def add_view(self, request, form_url="", extra_context=None):
        form = ProductForm()
        if request.POST:
            if "data" in request.POST:
                with transaction.atomic():
                    res = request.POST["data"]
                    res = json.loads(res)
                    RP = res["RP"]
                    PRD = Product.objects.get(RP=RP)
                    try:
                        vars = res["vars"]
                        for item in vars:
                            VAR = Variety()
                            VAR.ColorCode = item["ColorCode"]
                            VAR.ColorName = item["ColorName"]
                            VAR.Product = PRD
                            VAR.save()
                            for s in item["VarietySubs"]:
                                SI = VarietySub()
                                SI.Variety = VAR
                                SI.Size = s["Size"]
                                SI.Quantity = int(s["Quantity"])
                                SI.Discount = int(s["Discount"])
                                SI.FinalPrice = (100 - int(s["Discount"]) / 100) * PRD.BasePrice
                                SI.OffPrice = (int(s["Discount"]) / 100) * PRD.BasePrice
                                SI.save()
                        techs = res["Techs"]
                        for item in techs:
                            print(item)
                            name = item["key"]
                            value = item["value"]
                            if name != "" and value != "":
                                try:
                                    ProductTech.objects.get(Product=PRD, Name=name, Value=value)
                                except:
                                    PT = ProductTech()
                                    PT.Value = value
                                    PT.Name = name
                                    PT.Product = PRD
                                    PT.save()
                        fils = res["Filters"]
                        for item in fils:
                            if item["PK"] == "new":
                                Fil = Filters()
                                Fil.Category = PRD.Category
                                Fil.Name = item["Name"]
                                Fil.save()
                                FilV = FilterValue()
                                FilV.Filter = Fil
                                FilV.Title = item["Value"]
                                FilV.save()
                            else:
                                FilV = FilterValue.objects.get(pk=int(item["PK"]))
                            try:
                                FilP = ProductFilter.objects.get(Product=PRD, Filter=FilV)
                            except:
                                FilP = ProductFilter()
                                FilP.Product = PRD
                                FilP.Filter = FilV
                                FilP.save()
                        stat = 200
                    except:
                        stat = 500
                    return JsonResponse({"stat": stat})
            else:
                with transaction.atomic():
                    form = ProductForm(request.POST)
                    if form.is_valid():
                        PRD = Product()
                        PRD.Name = form.cleaned_data["Name"]
                        PRD.Category = form.cleaned_data["Category"]
                        PRD.Brand = form.cleaned_data["Brand"]
                        PRD.BasePrice = form.cleaned_data["BasePrice"]
                        PRD.Discount = form.cleaned_data["Discount"]
                        PRD.Description = form.cleaned_data["Description"]
                        PRD.Demo = form.cleaned_data["Demo"]
                        PRD.MetaDescription = form.cleaned_data["MetaDescription"]
                        PRD.MetaTitle = form.cleaned_data["MetaTitle"]
                        PRD.MetaKeywords = form.cleaned_data["MetaKeywords"]
                        PRD.save()
                        date = jdatetime.datetime.now().strftime("%Y%m%d")
                        RP = f"RP-{date}{PRD.pk}"
                        inp = Digits()
                        inpu = Digits()
                        slug = Slugify("Product", inp, inpu)
                        PRD.Slug = slug
                        PRD.RP = RP
                        PRD.save()
                        tags = request.POST["tags"]
                        tags = tags.split("-")
                        if len(tags) < 3:
                            raise ValidationError(
                                "تعداد کلمات کلید کمتر از ۳ عدد است و یا کلمات به درستی تفکیک نشده اند"
                            )
                        else:
                            for i in tags:
                                try:
                                    ProductTag.objects.get(Title=i)
                                except:
                                    tg = ProductTag()
                                    tg.Product = PRD
                                    tg.Title = i
                                    tg.save()
                        images = request.FILES.getlist("PRD_Images", False)
                        if not images or len(images) < 3 or len(images) > 5:
                            raise ValidationError(
                                "تعداد تصاویر مجاز نیست.بین ۳ تا ۵ تصویر مجاز است"
                            )
                        else:
                            for index, item in enumerate(images):
                                PIM = ProductImage()
                                PIM.Image = item
                                PIM.Product = PRD
                                if index == 0:
                                    PIM.Primary = True
                                PIM.save()
                    else:
                        print(form.errors)
                        return render(request, self.add_form_template, context=context)
                    return JsonResponse({"RP": RP})
        context = self.get_changeform_initial_data(request)
        context["form"] = form
        context.update(self.admin_site.each_context(request))
        return render(request, self.add_form_template, context)

    def change_view(self, request, object_id, form_url="", extra_context=""):
        PRD = (
            Product.objects.filter(pk=object_id)
            .prefetch_related(
                "image_prd",
                "tag_prd",
                "tech_prd",
                "variety_product",
                "fil_prd",
            )
            .first()
        )

        VarietySubS = []
        for item in PRD.variety_product.all():
            SI = VarietySub.objects.filter(Variety=item)
            VarietySubS.append(SI)
        form = ProductForm(instance=PRD)
        if request.POST:
            if "data" in request.POST:
                try:
                    res = request.POST["data"]
                    res = json.loads(res)
                    RP = res["RP"]
                    PRD = Product.objects.get(RP=RP)
                    vars = res["vars"]
                    for item in vars:
                        print(item)
                        try:
                            VAR = Variety.objects.get(RPV=item["RPV"])
                            pass
                        except:
                            VAR = Variety()
                        VAR.ColorCode = item["ColorCode"]
                        VAR.ColorName = item["ColorName"]
                        VAR.Product = PRD
                        VAR.save()
                        for s in item["VarietySubs"]:
                            try:
                                SI = VarietySub.objects.get(
                                    Variety=VAR,
                                    Size=s["Size"],
                                    Quantity=int(s["Quantity"]),
                                    Discount=int(s["Discount"]),
                                )
                            except:
                                SI = VarietySub()
                            SI.Variety = VAR
                            SI.Size = s["Size"]
                            SI.Quantity = int(s["Quantity"])
                            SI.Discount = int(s["Discount"])
                            SI.FinalPrice = (100 - int(s["Discount"]) / 100) * PRD.BasePrice
                            SI.OffPrice = (int(s["Discount"]) / 100) * PRD.BasePrice
                            SI.save()
                    techs = res["Techs"]
                    for item in techs:
                        print(item)
                        name = item["key"]
                        value = item["value"]
                        if name != "" and value != "":
                            try:
                                ProductTech.objects.get(Product=PRD, Name=name, Value=value)
                            except:
                                PT = ProductTech()
                                PT.Value = value
                                PT.Name = name
                                PT.Product = PRD
                                PT.save()
                    fils = res["Filters"]
                    for item in fils:
                        if item["PK"] == "new":
                            Fil = Filters()
                            Fil.Category = PRD.Category
                            Fil.Name = item["Name"]
                            Fil.save()
                            FilV = FilterValue()
                            FilV.Filter = Fil
                            FilV.Title = item["Value"]
                            FilV.save()
                        else:
                            FilV = FilterValue.objects.get(pk=int(item["PK"]))
                        try:
                            FilP = ProductFilter.objects.get(Product=PRD, Filter=FilV)
                        except:
                            FilP = ProductFilter()
                            FilP.Product = PRD
                            FilP.Filter = FilV
                            FilP.save()

                    stat = 200
                except:
                    stat = 500
                return JsonResponse({"stat": stat})
            elif "DeleteSizeDeactive" in request.POST:
                RPVS = request.POST["RPVS"]
                si = VarietySub.objects.get(RPVS=RPVS)
                si.Active = False
                si.save()
                return redirect(f"/admin/Products/product/{object_id}/change")
            elif "DeleteSizeDelete" in request.POST:
                RPVS = request.POST["RPVS"]
                si = VarietySub.objects.get(RPVS=RPVS)
                si.delete()
                return redirect(f"/admin/Products/product/{object_id}/change")
            elif "ActiveSize" in request.POST:
                RPVS = request.POST["RPVS"]
                si = VarietySub.objects.get(RPVS=RPVS)
                si.Active = True
                si.save()
                return redirect(f"/admin/Products/product/{object_id}/change")
            elif "DeleteVarDeactive" in request.POST:
                RPV = request.POST["RPV"]
                var = Variety.objects.filter(RPV=RPV).prefetch_related("size_var").first()
                var.Active = False
                var.save()
                for item in var.size_var.all():
                    item.Active = False
                    item.save()
                return redirect(f"/admin/Products/product/{object_id}/change")
            elif "DeleteVarDelete" in request.POST:
                RPV = request.POST["RPV"]
                var = Variety.objects.filter(RPV=RPV).prefetch_related("size_var").first()
                var.delete()
                return redirect(f"/admin/Products/product/{object_id}/change")
            elif "ImageDelete" in request.POST:
                RPI = request.POST["RPI"]
                Img = ProductImage.objects.filter(Product=PRD)
                if Img.count() > 3:
                    im = Img.filter(RPI=RPI).first()
                    im.delete()
                    if not Img.filter(Primary=True).exists():
                        im = Img.first()
                        im.Primary = True
                        im.save()
                else:
                    messages.error(
                        request, "تعداد تصاویر کمتر از ۳ عدد می باشد.حذف تصویر امکان پذیر نیست"
                    )

                return redirect(f"/admin/Products/product/{object_id}/change")
            elif "ImageEdit" in request.POST:
                RPI = request.POST["RPI"]
                img = request.FILES["Image_File"]
                Img = ProductImage.objects.get(RPI=RPI)
                Img.Image = img
                Img.save()
                return redirect(f"/admin/Products/product/{object_id}/change")
            elif "ActiveVar" in request.POST:
                RPV = request.POST["RPV"]
                var = Variety.objects.filter(RPV=RPV).prefetch_related("size_var").first()
                var.Active = True
                var.save()
                for item in var.size_var.all():
                    item.Active = True
                    item.save()
                return redirect(f"/admin/Products/product/{object_id}/change")
            else:
                form = ProductForm(request.POST)
                with transaction.atomic():
                    if form.is_valid():
                        PRD.Name = form.cleaned_data["Name"]
                        PRD.Category = form.cleaned_data["Category"]
                        PRD.Brand = form.cleaned_data["Brand"]
                        PRD.BasePrice = form.cleaned_data["BasePrice"]
                        PRD.Discount = form.cleaned_data["Discount"]
                        PRD.Description = form.cleaned_data["Description"]
                        PRD.Demo = form.cleaned_data["Demo"]
                        PRD.MetaDescription = form.cleaned_data["MetaDescription"]
                        PRD.MetaTitle = form.cleaned_data["MetaTitle"]
                        PRD.MetaKeywords = form.cleaned_data["MetaKeywords"]
                        PRD.save()
                        tags = request.POST["tags"]
                        tags = tags.split("-")
                        if len(tags) < 3:
                            raise ValidationError(
                                "تعداد کلمات کلید کمتر از ۳ عدد است و یا کلمات به درستی تفکیک نشده اند"
                            )
                        else:
                            for i in tags:
                                try:
                                    ProductTag.objects.get(Title=i)
                                except:
                                    if i != "":
                                        tg = ProductTag()
                                        tg.Product = PRD
                                        tg.Title = i
                                        tg.save()
                        images = request.FILES.getlist("PRD_Images", False)
                        PIMC = ProductImage.objects.filter(Product=PRD)

                        if images:
                            if len(PIM) < 5:
                                for index, item in enumerate(images):
                                    PIM = ProductImage()
                                    PIM.Image = item
                                    PIM.Product = PRD
                                    if index == 0 and PIMC.filter(Primary=True).count() == 0:
                                        PIM.Primary = True
                                    PIM.save()
                            else:
                                raise ValidationError(
                                    "تعداد تصاویر مجاز نیست.بین ۳ تا ۵ تصویر مجاز است"
                                )
                    else:
                        return render(request, self.add_form_template, context=context)
                return JsonResponse({"RP": PRD.RP})
        context = self.get_changeform_initial_data(request)
        context.update(self.admin_site.each_context(request))
        context["PRD"] = PRD
        context["VarietySubS"] = VarietySubS
        context["Tags"] = PRD.tag_prd.all()
        context["Techs"] = PRD.tech_prd.all()
        context["form"] = form
        return render(request, self.add_form_template, context=context)


class CategoryInline(admin.TabularInline):
    model = Category


class CategoryAdmin(MPTTModelAdmin):
    list_display = [
        "Name",
        "parent",
    ]
    inlines = [
        CategoryInline,
    ]


@admin.register(CategoryToPreview)
class CategoryToPreviewAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin View for ProductImage"""

    list_display = [
        "Product",
        "Image",
        "Primary",
    ]


@admin.register(ProductToPreview)
class ProductToPreviewAdmin(admin.ModelAdmin):
    list_display = [
        "Product",
        "Image",
        "Created_at",
    ]
    list_filter = ("Created_at",)
    readonly_fields = ["Image", "Varities"]
    ordering = ("Created_at",)


@admin.register(TopSellToPreview)
class TopSellToPreviewAdmin(admin.ModelAdmin):
    list_display = [
        "Product",
        "Image",
        "Created_at",
    ]
    list_filter = ("Created_at",)
    readonly_fields = ["Image", "Varities"]
    ordering = ("Created_at",)


admin.site.register(Category, CategoryAdmin)


@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    list_display = ("Product", "RPV")
    inlines = [
        VarietySubInline,
    ]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["Name"]


@admin.register(Guarantee)
class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ["Name"]


@admin.register(BrandToPreview)
class BrandToPreviewAdmin(admin.ModelAdmin):
    list_display = ("Name",)
    readonly_fields = ("Name",)


@admin.register(Testimotional)
class TestimotionalAdmin(admin.ModelAdmin):
    list_display = ("Name",)
    readonly_fields = ("Name",)
    ordering = ("Created_at",)
