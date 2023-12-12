from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
@receiver(post_save, sender=Post())
def create_Post()(sender, instance, created, *args, **kwargs):
    if created:
        RP = instance.Product.RP
        RP = RP.split("RP-")
        RP = RP[1]
        Count = Post().objects.filter(Product=instance.Product).count()
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

