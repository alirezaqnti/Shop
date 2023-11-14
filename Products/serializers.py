from rest_framework import serializers
from .models import (
    ProductToPreview,
    Product,
    ProductImage,
    Variety,
    ProductStat,
    Filters,
    Category,
    VarietySub,
)
import json


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        res = []
        for item in Category.objects.filter(parent_id=obj.pk):
            child = {}
            child["parent"] = item.to_json()
            child["children"] = []
            for c in item.get_descendants(include_self=False):
                child["children"].append(c.to_json())
            res.append(child)
        print(res)
        return res

    class Meta:
        model = Category
        fields = "__all__"


class ProductToPreviewSerializer(serializers.ModelSerializer):
    Product_Name = serializers.CharField(source="Product.Name")
    Product_BasePrice = serializers.CharField(source="Product.BasePrice")
    slug = serializers.CharField(source="Product.Slug")
    RP = serializers.CharField(source="Product.RP")
    Image_URL = serializers.CharField(source="Image.Image")

    class Meta:
        model = ProductToPreview
        fields = [
            "slug",
            "Product_Name",
            "Image_URL",
            "Created_at",
            "Product_BasePrice",
            "Varities",
            "RP",
        ]


class ProductSerializer(serializers.ModelSerializer):
    Varities = serializers.SerializerMethodField()
    Image_URL = serializers.SerializerMethodField()
    FinalPrice = serializers.SerializerMethodField()

    def get_FinalPrice(self, obj):
        vrs = Variety.objects.filter(Product=obj, Active=True, Status=ProductStat.valid).first()
        VarietySubs = VarietySub.objects.filter(Variety=vrs).first()
        return VarietySubs.FinalPrice

    def get_Varities(self, obj):
        vrs = Variety.objects.filter(Product=obj, Active=True, Status=ProductStat.valid)
        data = []
        for item in vrs:
            VarietySubs = VarietySub.objects.filter(Variety=item).order_by("Size")
            si = []
            for size in VarietySubs:
                si.append(
                    {
                        "Size": size.Size,
                        "Quantity": size.Quantity,
                        "Discount": size.Discount,
                        "OffPrice": size.OffPrice,
                        "FinalPrice": size.FinalPrice,
                        "RPVS": size.RPVS,
                    }
                )
            data.append(
                {
                    "RPV": item.RPV,
                    "Color": item.ColorCode,
                    "Size": si,
                }
            )
        data = json.dumps(data)
        return data

    def get_Image_URL(self, obj):
        print("OBJ:", obj)
        image = ProductImage.objects.get(Product=obj, Primary=True)
        return str(image.Image)

    class Meta:
        model = Product
        fields = [
            "Slug",
            "Name",
            "Image_URL",
            "Created_at_g",
            "BasePrice",
            "Varities",
            "RP",
            "Visit",
            "FinalPrice",
        ]


class FiltersSerializer(serializers.ModelSerializer):
    Filter = serializers.SerializerMethodField()

    def get_Filter(self, obj):
        filters = Filters.objects.filter(Category=obj)
        material = {
            "Name": "جنس",
            "Queries": [],
        }
        type = {
            "Name": "نوع",
            "Queries": [],
        }
        usage = {
            "Name": "مورد استفاده",
            "Queries": [],
        }
        heels = {
            "Name": "نوع پاشنه",
            "Queries": [],
        }
        shoelace = {
            "Name": "نحوه بسته شدن کفش",
            "Queries": [],
        }
        strap = {
            "Name": "بند و دستگیره",
            "Queries": [],
        }
        form = {
            "Name": "فرم کیف",
            "Queries": [],
        }
        print(filters)
        for item in filters:
            print(item.Type)
            if item.Type == 2:
                material["Queries"].append({"Name": item.Name, "pk": item.pk})
            elif item.Type == 3:
                type["Queries"].append({"Name": item.Name, "pk": item.pk})
            elif item.Type == 4:
                usage["Queries"].append({"Name": item.Name, "pk": item.pk})
            elif item.Type == 5:
                heels["Queries"].append({"Name": item.Name, "pk": item.pk})
            elif item.Type == 6:
                shoelace["Queries"].append({"Name": item.Name, "pk": item.pk})
            elif item.Type == 7:
                strap["Queries"].append({"Name": item.Name, "pk": item.pk})
            elif item.Type == 8:
                form["Queries"].append({"Name": item.Name, "pk": item.pk})

        res = {}
        if len(material["Queries"]) > 0:
            res["material"] = material
        if len(type["Queries"]) > 0:
            res["type"] = type
        if len(usage["Queries"]) > 0:
            res["usage"] = usage
        if len(heels["Queries"]) > 0:
            res["heels"] = heels
        if len(shoelace["Queries"]) > 0:
            res["shoelace"] = shoelace
        if len(strap["Queries"]) > 0:
            res["strap"] = strap
        if len(form["Queries"]) > 0:
            res["form"] = form

        return res

    class Meta:
        model = Category
        fields = [
            "Filter",
        ]


class VarietySerializer(serializers.ModelSerializer):
    BasePrice = serializers.IntegerField(source="Product.BasePrice")
    Size = serializers.SerializerMethodField()

    def get_Size(self, obj):
        VarietySubs = VarietySub.objects.filter(Variety=obj)
        data = []
        for item in VarietySubs:
            data.append(
                {
                    "Size": item.Size,
                    "Quantity": item.Quantity,
                    "Discount": item.Discount,
                    "FinalPrice": item.FinalPrice,
                    "OffPrice": item.OffPrice,
                    "RPVS": item.RPVS,
                }
            )
        print(data)
        return data

    class Meta:
        model = Variety
        fields = [
            "Product",
            "RPV",
            "BasePrice",
            "ColorCode",
            "Active",
            "Status",
            "Size",
        ]
