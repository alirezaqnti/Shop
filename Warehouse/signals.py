from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart, CartProduct, WishList, Coupon, WheelOfFortune, FortunePrize
from datetime import datetime
from random import randint
from django.core.cache import cache


@receiver(post_save, sender=WheelOfFortune)
def create_WheelOfFortune(sender, instance, created, *args, **kwargs):
    if created:
        WH = (
            WheelOfFortune.objects.filter(Active=True)
            .exclude(pk=instance.pk)
            .update(Active=False)
        )


@receiver(post_save, sender=FortunePrize)
def create_FortunePrize(sender, instance, created, *args, **kwargs):
    if created:
        Cou = Coupon()
        Cou.MaxPrice = instance.Price
        Cou.Time = instance.Wheel.Date
        Cou.save()
        instance.Coupon = Cou
        instance.RFP = Cou.Code
        instance.save()


@receiver(post_save, sender=WishList)
def create_WishList(sender, instance, created, *args, **kwargs):
    if created:
        d = datetime.now().strftime("%M%S")
        RC = f"RW-{d}{str(randint(1000,9999))}"
        instance.RW = RC
        instance.save()


@receiver(post_save, sender=Cart)
def create_Cart(sender, instance, created, *args, **kwargs):
    if created:
        d = datetime.now().strftime("%M%S")
        RC = f"RC-{d}{str(randint(1000,9999))}"
        instance.RC = RC
        instance.save()


@receiver(post_save, sender=CartProduct)
def create_CartProduct(sender, instance, created, *args, **kwargs):
    if created:
        Count = CartProduct.objects.filter(Cart=instance.Cart).count()
        RC = instance.Cart.RC
        RC = RC.split("RC-")
        RC = RC[1]
        while True:
            RCP = f"RCP-{RC}{str(Count)}"
            try:
                CartProduct.objects.get(RCP=RCP)
            except:
                break
            Count += 1
        instance.RCP = RCP
        instance.save()
