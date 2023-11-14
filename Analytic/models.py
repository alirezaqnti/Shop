from django.db import models
from Users.models import UserInfo
from django.utils.translation import gettext as _


class Visit(models.Model):
    IP = models.CharField(max_length=16)
    User = models.ForeignKey(UserInfo, on_delete=models.CASCADE, blank=True, null=True)
    URL = models.URLField(max_length=400)
    Created_AT = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Visit")
        verbose_name_plural = _("Visits")

    def __str__(self):
        return self.IP
