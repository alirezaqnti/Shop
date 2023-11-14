from rest_framework import serializers
from .models import UserInfo

import rsa

pbKEYn = 7103911361751289296658388830746844227983219246289797730958985648971967279708296739736792579263687929546606918383482400680235043342107525818413503464325971
pbKEYe = 65537
prKEYd = 2972311113578316123772367977293883082465292200627318058205690609586345341519248303895066173321944931813135020998013444255269957602943741946502311933902073
prKEYp = 4731199765390719506094051066379241046338305937891657841571405284305548516145942981
prKEYq = 1501503152269585625202396327858355883810508305252554689784338601803188791


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["Phone", "Name", "Password", "Phone_Confirm", "Gender"]

        def validate(self, data):
            if UserInfo.objects.filter(Phone=data["Phone"]).exists():
                raise serializers.ValidationError("کاربر دیگری با این تلفن همراه ثبت شده است")

            return data


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = [
            "Phone",
        ]


class UserLoginSerializer(serializers.Serializer):
    Phone = serializers.CharField(required=False, allow_blank=True)
    Password = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        try:
            obj = UserInfo.objects.get(Phone=data["Phone"])
            privateKey = rsa.PrivateKey(pbKEYn, pbKEYe, prKEYd, prKEYp, prKEYq)
            Pass = rsa.decrypt(obj.key, privateKey).decode()
            if Pass == data["Password"]:
                return data
        except:
            raise serializers.ValidationError("Wrong Pass!")
