from datetime import datetime

from rest_framework import serializers

from .models import *

from .models import Offers
from Products.models import ProductStat, Product, VarietySub


def DateDif(d1, time):
    d2 = datetime.now()
    dif = (d2 - d1.replace(tzinfo=None)).total_seconds()
    if dif < time:
        return True
    else:
        return False


class PhoneCodeRegSerializer(serializers.ModelSerializer):
    Phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CodeReg
        fields = ["Code", "Phone"]

    def validate(self, data):
        code = CodeReg.objects.get(Code=data["Code"], Phone=data["Phone"], Active=True)
        dif = DateDif(code.Created_At, 300)
        if not dif:
            code.Active = False
            code.save()
            raise serializers.ValidationError("کد وارد شده منقضی شده است")
        code.Active = False
        code.save()
        try:
            return True
        except:
            raise serializers.ValidationError("کد وارد شده صحیح نیست")


class OfferSerializer(serializers.ModelSerializer):
    Varities = serializers.SerializerMethodField()
    Images = serializers.SerializerMethodField()
    Product = serializers.SerializerMethodField()
    Default = serializers.SerializerMethodField()

    def get_Default(self, obj):
        Sub = obj.Sub
        Var = Sub.Variety
        Default = {
            "RPV": Var.RPV,
            "ColorCode": Var.ColorCode,
            "ColorName": Var.ColorName,
            "Size": Sub.Size,
            "Quantity": Sub.Quantity,
            "Discount": Sub.Discount,
            "OffPrice": Sub.OffPrice,
            "FinalPrice": Sub.FinalPrice,
            "RPVS": Sub.RPVS,
        }
        return Default

    def get_Product(self, obj):
        PR = (
            Product.objects.filter(RP=obj.Product.RP)
            .prefetch_related("variety_product")
            .first()
        )
        return {
            "Slug": PR.Slug,
            "Name": PR.Name,
            "Created_at_g": str(PR.Created_at_g),
            "BasePrice": PR.BasePrice,
            "RP": PR.RP,
            "Visit": PR.Visit,
            "Demo": PR.Demo,
            "Rate": range(PR.Rate),
        }

    def get_Varities(self, obj):
        PR = (
            Product.objects.filter(RP=obj.Product.RP)
            .prefetch_related("variety_product")
            .first()
        )

        vrs = PR.variety_product.filter(Active=True, Status=ProductStat.valid)
        Vars = []
        Default = {}
        Lables = []
        for item in vrs:
            if VarietySub.objects.filter(Variety=item, Quantity__gte=0).exists():
                Sub = VarietySub.objects.filter(Variety=item, Quantity__gte=0).first()

                if Sub.Discount > 0:
                    Lables.append(
                        {
                            "Lable": "label-sale",
                            "Value": Sub.Discount,
                        }
                    )
            else:
                Sub = VarietySub.objects.filter(Variety=vrs).first()
                Lables.append({"Lable": "prd-outstock"})
            Vars.append(
                {
                    "RPV": item.RPV,
                    "ColorCode": item.ColorCode,
                    "ColorName": item.ColorName,
                    "RPVS": Sub.RPVS,
                }
            )

        data = {
            "Lables": Lables,
            "Vars": Vars,
        }
        return data

    def get_Images(self, obj):
        PR = (
            Product.objects.filter(RP=obj.Product.RP)
            .prefetch_related("image_prd")
            .first()
        )
        images = PR.image_prd.all().order_by("-Primary")[:3]
        res = []
        for item in images:
            res.append({"Image": str(item.Image), "Primary": str(item.Primary)})
        return res

    class Meta:
        model = Offers
        fields = [
            "Product",
            "Default",
            "Varities",
            "Images",
        ]
