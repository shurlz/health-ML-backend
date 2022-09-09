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
    Age = serializers.IntegerField(required=True, min_value=0, max_value=120)
    Sex = serializers.CharField(required=True)
    ChestPainType = serializers.CharField(required=True)
    RestingBP = serializers.FloatField(required=True, min_value=0, max_value=200)
    Cholesterol = serializers.FloatField(required=True, min_value=0, max_value=620)
    FastingBS = serializers.FloatField(required=True, min_value=0, max_value=1)
    RestingECG = serializers.CharField(required=True)
    MaxHR = serializers.FloatField(required=True, min_value=50, max_value=210)
    ExerciseAngina = serializers.CharField(required=True)
    Oldpeak = serializers.FloatField(required=True, min_value=-5, max_value=10)
    ST_Slope = serializers.CharField(required=True)

class StrokeDataSerializer(Serializer):
    pass

class HepatitisDataSerializer(Serializer):
    Age = serializers.IntegerField(required=True, min_value=0, max_value=120)
    Sex = serializers.CharField(required=True)
    ALB = serializers.FloatField(required=True, min_value=0, max_value=85)
    ALP = serializers.FloatField(required=True, min_value=0, max_value=420)
    ALT = serializers.FloatField(required=True, min_value=0, max_value=330)
    AST = serializers.FloatField(required=True, min_value=0, max_value=330)
    BIL = serializers.FloatField(required=True, min_value=0, max_value=260)
    CHE = serializers.FloatField(required=True, min_value=0, max_value=20)
    CHOL = serializers.FloatField(required=True, min_value=0, max_value=10)
    CREA = serializers.FloatField(required=True, min_value=0, max_value=1100)
    GGT = serializers.FloatField(required=True, min_value=0, max_value=660)
    PROT = serializers.FloatField(required=True, min_value=40, max_value=100)

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

        