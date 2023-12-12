from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
import string, random
import jdatetime
from Users.models import UserInfo


def get_random_string():
    letters = string.ascii_uppercase
    result_str = "".join(random.choice(letters) for i in range(6))
    return result_str


def JDATE():
    return jdatetime.datetime.today().strftime("%m-%d")


class Post(models.Model):
    RPO = models.CharField(_("شماره پست"), max_length=50, default=get_random_string)
    Title = models.CharField(_("عنوان"), max_length=200, null=True, blank=True)
    Author = models.CharField(_("نویسنده"), max_length=200, null=True, blank=True)
    Text = RichTextUploadingField(_("متن"), null=True, blank=True)
    Demo = models.TextField(_("دمو"), null=True, blank=True)
    Poster = models.ImageField(_("پوستر"), upload_to="Blog/", null=True, blank=True)
    MetaKeyWords = models.CharField(max_length=80, null=True, blank=True)
    MetaDescription = models.CharField(max_length=360, null=True, blank=True)
    MetaTitle = models.CharField(max_length=50, null=True, blank=True)
    Rate = models.IntegerField(_("امتیاز"), default=0)
    Created_At = models.DateTimeField(auto_now_add=True)
    Created = models.CharField(
        _("تاریخ ثبت"), max_length=50, null=True, blank=True, default=JDATE
    )
    Modified_At = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name_plural = _("پست ها")

    def __str__(self):
        return self.Title


class PostTags(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tag_post")
    Value = models.CharField(_("کلمه"), max_length=50)
    ClickCount = models.IntegerField(_("تعداد کلیک برچسب"), default=0)
    Usage = models.IntegerField(_("تعداد استفاده از تگ"), default=1)
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name_plural = _("تگ های پست")

    def __str__(self):
        return self.Value


class PostComment(models.Model):
    Post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comment_post"
    )
    Phone = models.CharField(max_length=11)
    Name = models.CharField(max_length=100)
    Text = models.TextField(max_length=500, blank=True, null=True)
    Rate = models.IntegerField(_("امتیاز"), default=0)
    Created_At = models.DateTimeField(auto_now_add=True)
    Created = models.CharField(
        _("تاریخ ثبت"), max_length=50, null=True, blank=True, default=JDATE
    )
    Modified_At = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(_("فعال"), default=True)

    class Meta:
        verbose_name_plural = _("کامنت های پست")


class PostRate(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="rate_post")
    User = models.ForeignKey(
        UserInfo, verbose_name=_("کاربر"), on_delete=models.CASCADE
    )
    IP = models.CharField(max_length=15, blank=True, null=True)
    Active = models.BooleanField(_("فعال"), default=True)
