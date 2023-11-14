import random, string

import jdatetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _


def UsersProfile(instance, name):
    return f"Users/{instance.Parent.Email}/ProfileImage/{name}"


def JDATE():
    return jdatetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")


def Slugify(Email, Phone):
    val1 = list(Email)
    val2 = list(Phone)
    res = val1 + val2
    random.shuffle(res)
    listToStr = "".join(map(str, res))
    slug = "User-" + listToStr
    return slug


def get_random_string():
    letters = string.ascii_uppercase
    result_str = "".join(random.choice(letters) for i in range(6))
    return result_str


class GenderType(models.IntegerChoices):
    Male = (1,)
    Female = (2,)


class UserInfo(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)
    Phone = models.CharField(_("شماره تماس"), max_length=13, unique=True)
    Password = models.CharField(_("رمز عبور"), max_length=250)
    key = models.BinaryField(blank=True, null=True, max_length=200)
    Name = models.CharField(_("نام"), max_length=100)
    Iban = models.CharField(_("شماره شبا"), max_length=26, blank=True, null=True)
    Gender = models.IntegerField(_("جنسیت"), default=GenderType.Female, choices=GenderType.choices)
    CreaditCard = models.CharField(_("شماره کارت"), max_length=16, blank=True, null=True)
    ProfileImage = models.ImageField(
        _("تصویر پروفایل"),
        upload_to=UsersProfile,
        max_length=100,
        blank=True,
        null=True,
    )
    Phone_Confirm = models.BooleanField(_("تاییدیه موبایل"), default=False)
    Email_Confirm = models.BooleanField(_("تاییدیه ایمیل"), default=False)
    Joined_At = models.DateTimeField(_("تاریخ عضویت"), auto_now_add=True, editable=False)
    Joined_At_J = models.CharField(_("تاریخ عضویت"), max_length=100, default=JDATE, editable=False)
    Left_At = models.DateTimeField(
        _("تاریخ قطع همکاری"), auto_now_add=False, blank=True, null=True
    )
    Modified_At = models.DateTimeField(_("تاریخ اخرین تغییر"), auto_now_add=True)
    Modified_At_J = models.CharField(_("تاریخ اخرین تغییر"), max_length=100, blank=True, null=True)
    Last_Login = models.DateTimeField(_("اخرین ورود"), auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = _("کاربران")

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        rs = get_random_string()
        try:
            if not self.pk:
                self.slug = Slugify(rs, self.Phone)
            return super(UserInfo, self).save(*args, **kwargs)
        except:
            if not self.pk:
                self.slug = Slugify(rs, self.Phone)
            return super(UserInfo, self).save(*args, **kwargs)

    def toJson(self, *args, **kwargs):
        return {
            "slug": self.slug,
            "Phone": self.Phone,
            "Password": self.Password,
            "Name": self.Name,
            "Iban": self.Iban,
            "CreaditCard": self.CreaditCard,
            "ProfileImage": str(self.ProfileImage),
        }


class Userlogs(models.Model):
    Parent = models.ForeignKey(UserInfo, verbose_name=_("والد"), on_delete=models.CASCADE)
    Data = RichTextUploadingField(_("دیتا"), blank=True, null=True)
    Created_At = models.DateTimeField(_("تاریخ عضویت"), auto_now_add=True, editable=False)
    Created_At_J = models.CharField(
        _("تاریخ عضویت"), max_length=100, default=JDATE, editable=False
    )

    class Meta:
        verbose_name_plural = _("Userlogs")

    def __str__(self):
        return self.Parent.FirstName + self.Parent.LastName
