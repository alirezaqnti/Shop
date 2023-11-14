from datetime import datetime

from rest_framework import serializers

from .models import *

from Warehouse.models import WheelOfFortune


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
