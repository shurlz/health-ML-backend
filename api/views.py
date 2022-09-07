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

@api_view(['GET'])
def connect(request):
    return JsonResponse({'status':'connected...'})

@api_view(['POST','GET'])
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
    return JsonResponse({'response':'signup successful'})

@api_view(['POST','GET'])
def heartPredictor(request):   
    serializer = HeartDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    model = heartFunc(Age=request.data['Age'], Sex=request.data['Sex'], ChestPainType=request.data['ChestPainType'],
                        RestingBP=request.data['RestingBP'], Cholesterol=request.data['Cholesterol'], FastingBS=request.data['FastingBS'],
                            RestingECG=request.data['RestingECG'], MaxHR=request.data['MaxHR'], ExerciseAngina=request.data['ExerciseAngina'],
                            Oldpeak=request.data['Oldpeak'], ST_Slope=request.data['ST_Slope'])    
    model_result = 'positive' if model == 1 else 'negative'
    
    if request.user.is_authenticated:
        user_serializer = userHistory(owner=request.user , test_name='Heart Disease', result=model_result)
        user_serializer.save()

    return JsonResponse({'prediction':f'{model_result}'})

@api_view(['POST','GET'])
def hepatitisPredictor(request):
    serializer = HepatitisDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    model = hepatitisFunc(Age=request.data['Age'], Sex=request.data['Sex'], ALB=request.data['ALB'],
                            ALP=request.data['ALP'], ALT=request.data['ALT'], AST=request.data['AST'],
                            BIL=request.data['BIL'], CHE=request.data['CHE'], CHOL=request.data['CHOL'],
                            CREA=request.data['CREA'], GGT=request.data['GGT'], PROT=request.data['PROT'])    
    model_result = 'positive' if model == 1 else 'negative'
    
    if request.user.is_authenticated:
        user_serializer = userHistory(owner=request.user , test_name='Hepatitis Disease', result=model_result)
        user_serializer.save()

    return JsonResponse({'prediction':f'{model_result}'})

@api_view(['POST','GET'])
def strokePredictor(request):
    serializer = StrokeDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    model = ''#function .predict processed input
    return JsonResponse({'prediction':f'{model_result}'})

@api_view(['POST','GET'])
def signin(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _ , token = AuthToken.objects.create(user)

    return JsonResponse({'token':token})

@api_view(['POST','GET'])
def subscribe(request):
    serializer = subscribersSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST','GET'])
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

@api_view(['POST','GET'])
@permission_classes((IsAuthenticated,))
def user_history(request):
    user_history_data = userHistory.objects.filter(owner=request.user)
    serializer = userHistorySerializer(user_history_data,many=True)
    return Response(serializer.data)


