from rest_framework import serializers
from .models import WheelOfFortune, FortunePrize


class FortunePrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FortunePrize
        fields = [
            "RFP",
            "Title",
        ]


class WheelSerializer(serializers.ModelSerializer):
    Prizes = serializers.SerializerMethodField()

    def get_Prizes(self, obj):
        data = []
        for item in FortunePrize.objects.filter(Wheel=obj):
            data.append({"RFP": item.RFP, "Title": item.Title, "Null": item.Null})
        return data

    class Meta:
        model = WheelOfFortune
        fields = ["Prizes", "Date"]
