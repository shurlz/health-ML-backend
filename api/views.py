from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import HeartDataSerializer, StrokeDataSerializer, HepatitisDataSerializer, userHistorySerializer, subscribersSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .machine_learning import hepatitisFunc , heartFunc
from django.http import HttpResponse, JsonResponse
from .models import userHistory, subscribers
# Create your views here.

@api_view(['POST'])
def signup(request):
    username = request.data["username"]
    password = request.data["password"]
    confirm_password = request.data["confirm_password"]
    
    username_check = User.objects.filter(username=username).first()
    if username_check:
        return Response({'response':'username already exists'})
    
    if password != confirm_password:
        return Response({"response":"passwords do not match"})
    
    new_user = User(username=username)
    new_user.set_password(password)
    new_user.save()
    return Response({'response':'signup successful'})

@api_view(['POST'])
def heartPredictor(request):    
    serializer = HeartDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    model = heartFunc(request.data['Age'],request.data['Sex'],request.data['ChestPainType'],
                            request.data['RestingBP'],request.data['Cholesterol'],request.data['FastingBS'],
                            request.data['RestingECG'],request.data['MaxHR'],request.data['ExerciseAngina'],
                            request.data['Oldpeak'],request.data['ST_Slope'])    
    model_result = f'prediction is {model}'
    print(serializer.data)
    print(model_result)
    if request.user.is_authenticated:
        user_serializer = userHistorySerializer(owner=request.user , test_name='Heart Disease', result=model_result)
        user_serializer.save()

    return Response(model_result)

@api_view(['POST'])
def hepatitisPredictor(request):
    serializer = HepatitisDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    model = hepatitisFunc(request.data['Age'],request.data['Sex'],request.data['ALB'],
                            request.data['ALP'],request.data['ALT'],request.data['AST'],
                            request.data['BIL'],request.data['CHE'],request.data['CHOL'],
                            request.data['CREA'],request.data['GGT'],request.data['PROT'])    
    model_result = f'prediction is {model}'
    print(serializer.data)
    print(model_result)
    if request.user.is_authenticated:
        user_serializer = userHistorySerializer(owner=request.user , test_name='Hepatitis Disease', result=model_result)
        user_serializer.save()

    return Response(model_result)

@api_view(['POST'])
def strokePredictor(request):
    serializer = StrokeDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    model = ''#function .predict processed input
    return Response(model)

@api_view(['POST'])
def signin(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _ , token = AuthToken.objects.create(user)

    return Response({'token':f'{token}'})

@api_view(['POST'])
def subscribe(request):
    serializer = subscribersSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def unsubscribe(request):
    serializer = subscribersSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        email = subscribers.objects.filter(email=request.data["email"]).first()
        email.delete()
    except:
        return Response('you are not subscribed')
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_history(request):
    user_history_data = userHistory.objects.filter(owner=request.user)
    serializer = userHistorySerializer(user_history_data,many=True)
    return Response(serializer.data)


