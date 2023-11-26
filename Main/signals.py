from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Offers, ImageBox
from core.settings import REFFERER
from Products.models import ProductImage


@receiver(post_save, sender=ImageBox)
def create_ImageBox(sender, instance, created, *args, **kwargs):
    if created:
        if instance.Type == "0":
            instance.Url = f"{REFFERER}wheel-of-fortune/"
        if instance.Type == "2":
            instance.Url = f"{REFFERER}slide/{instance.RS}"
        instance.save()


@receiver(post_save, sender=Offers)
def create_Offers(sender, instance, created, *args, **kwargs):
    if created:
        if instance.Type == "2" and instance.Sub.Discount == 0:
            instance.delete()
        else:
            Pr = instance.Sub.Variety.Product
            instance.Product = Pr
            instance.save()
