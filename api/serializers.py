from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import User
from .models import userHistory, subscribers

class SignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "password"
        ]

class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "password"
        ]


class HeartDataSerializer(Serializer):
    Age = serializers.IntegerField()
    Sex = serializers.IntegerField()
    ChestPainType = serializers.IntegerField()
    RestingBP = serializers.IntegerField()
    Cholesterol = serializers.IntegerField()
    FastingBS = serializers.IntegerField()
    RestingECG = serializers.IntegerField()
    MaxHR = serializers.IntegerField()
    ExerciseAngina = serializers.IntegerField()
    Oldpeak = serializers.IntegerField()
    ST_Slope = serializers.IntegerField()

class StrokeDataSerializer(Serializer):
    pass

class HepatitisDataSerializer(Serializer):
    Age = serializers.IntegerField()
    Sex = serializers.IntegerField()
    ALB = serializers.IntegerField()
    ALP = serializers.IntegerField()
    ALT = serializers.IntegerField()
    AST = serializers.IntegerField()
    BIL = serializers.IntegerField()
    CHE = serializers.IntegerField()
    CHOL = serializers.IntegerField()
    CREA = serializers.IntegerField()
    GGT = serializers.IntegerField()
    PROT = serializers.IntegerField()

class userHistorySerializer(ModelSerializer):
    class Meta:
        model = userHistory
        fields = [
            "owner","test_name","result"
            ]

class subscribersSerializer(ModelSerializer):
    class Meta:
        model = subscribers
        fields = "__all__"

        