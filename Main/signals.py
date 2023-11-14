from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Shortener, QuickOffer, Slider
import pyshorteners
from core.settings import REFFERER
from Products.models import ProductImage


@receiver(post_save, sender=Shortener)
def create_Shortener(sender, instance, created, *args, **kwargs):
    if created:
        short = pyshorteners.Shortener()
        print(short)
        print(instance.Real)
        instance.Short = short.tinyurl.short(instance.Real)
        instance.save()


@receiver(post_save, sender=Slider)
def create_Slider(sender, instance, created, *args, **kwargs):
    if created:
        if instance.Type == "0":
            instance.Url = f"{REFFERER}wheel-of-fortune/"
        if instance.Type == "2":
            instance.Url = f"{REFFERER}slide/{instance.RS}"
        instance.save()


@receiver(post_save, sender=QuickOffer)
def create_QuickOffer(sender, instance, created, *args, **kwargs):
    if created:
        Pr = instance.Variety.Variety.Product
        Img = ProductImage.objects.filter(Product=Pr, Primary=True).first()
        instance.Image = Img.Image
        instance.Url = f"{REFFERER}products/{Pr.Slug}"
        instance.Name = Pr.Name
        instance.save()
