from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    Product,
    Variety,
    ProductImage,
    ProductToPreview,
    Testimotional,
    TopSellToPreview,
    VarietySub,
    Filters,
    Category,
    BrandToPreview,
    Testimotional,
    CategoryToPreview,
)
from django.core import serializers
import json


@receiver(post_save, sender=Variety)
def create_Variety(sender, instance, created, *args, **kwargs):
    if created:
        RP = instance.Product.RP
        RP = RP.split("RP-")
        RP = RP[1]
        Count = Variety.objects.filter(Product=instance.Product).count()
        RPV = f"RPV-{RP}{str(Count)}"
        instance.RPV = RPV
        instance.save()
        # try:
        #     Filters.objects.get(
        #         Category=instance.Product.Category, Type=0, Name=instance.ColorName
        #     )
        # except:
        #     Filters.objects.create(
        #         Category=instance.Product.Category, Type=0, Name=instance.ColorName
        #     )


@receiver(post_save, sender=Product)
def create_Product(sender, instance, created, *args, **kwargs):
    for item in VarietySub.objects.filter(Variety__Product=instance):
        i_FinalPrice = item.FinalPrice
        i_OffPrice = item.OffPrice
        if instance.Discount > 0 or item.Discount > 0:
            Discount = item.Discount
            if instance.Discount > item.Discount:
                Discount = instance.Discount
            price = instance.BasePrice * ((100 - Discount) / 100)
            offPrice = instance.BasePrice - price
            i_FinalPrice = price
            i_OffPrice = offPrice
        else:
            i_FinalPrice = instance.BasePrice
            i_OffPrice = 0
        VarietySub.objects.filter(pk=item.pk).update(OffPrice=i_OffPrice, FinalPrice=i_FinalPrice)


@receiver(post_save, sender=VarietySub)
def create_VarietySub(sender, instance, created, *args, **kwargs):
    if created:
        Var = instance.Variety
        count = VarietySub.objects.filter(Variety=Var).count()
        Prod = Var.Product
        Dis = Prod.Discount
        Base = Prod.BasePrice
        if instance.Discount > 0 or Dis > 0:
            Discount = instance.Discount
            if Dis > instance.Discount:
                Discount = Dis
            price = Base * ((100 - Discount) / 100)
            offPrice = Base - price
            instance.FinalPrice = price
            instance.OffPrice = offPrice
        else:
            instance.FinalPrice = Base
            instance.OffPrice = 0
        if instance.Size != None:
            instance.RPVS = Var.RPV + instance.Size + str(count)
        else:
            instance.RPVS = Var.RPV + str(count)
        instance.save()


@receiver(post_save, sender=ProductImage)
def create_ProductImage(sender, instance, created, *args, **kwargs):
    if created:
        img = ProductImage.objects.filter(Product=instance.Product).first()
        img.Primary = True
        img.save()


@receiver(post_save, sender=ProductToPreview)
def create_ProductToPreview(sender, instance, created, *args, **kwargs):
    if created:
        image = ProductImage.objects.get(Product=instance.Product, Primary=True)
        instance.Image = image
        varities = Variety.objects.filter(Product=instance.Product, Active=True)
        data = []
        for item in varities:
            qs = VarietySub.objects.filter(Variety=item).order_by("-Size")
            sizes = serializers.serialize("json", qs)
            data.append(
                {
                    "RPV": item.RPV,
                    "Color": item.ColorCode,
                    "Size": sizes,
                }
            )
        instance.Name = instance.Product.Name
        instance.Varities = json.dumps(data)
        instance.save()


@receiver(post_save, sender=TopSellToPreview)
def create_TopSellToPreview(sender, instance, created, *args, **kwargs):
    if created:
        image = ProductImage.objects.get(Product=instance.Product, Primary=True)
        instance.Image = image
        varities = Variety.objects.filter(Product=instance.Product, Active=True)
        data = []
        for item in varities:
            qs = VarietySub.objects.filter(Variety=item).order_by("-Size")
            sizes = serializers.serialize("json", qs)
            data.append(
                {
                    "RPV": item.RPV,
                    "Color": item.ColorCode,
                    "Size": sizes,
                }
            )
        instance.Varities = json.dumps(data)
        instance.Name = instance.Product.Name
        instance.save()


@receiver(post_save, sender=BrandToPreview)
def create_BrandToPreview(sender, instance, created, *args, **kwargs):
    if created:
        instance.Name = instance.Brand.Name
        instance.save()


@receiver(post_save, sender=Testimotional)
def create_Testimotional(sender, instance, created, *args, **kwargs):
    if created:
        instance.Name = instance.Comment.Product.Name
        instance.save()


@receiver(post_save, sender=CategoryToPreview)
def create_CategoryToPreview(sender, instance, created, *args, **kwargs):
    if created:
        instance.Name = instance.Category.Name
        instance.save()
