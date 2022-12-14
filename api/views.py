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


@api_view(['POST','GET'])
def signup(request):
    if request.method == 'POST':
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
    if request.method == 'GET':
        return Response({'connected..':'Make a POST request with the required parameters to retrieve a valid response'})

@api_view(['POST','GET'])
def heartPredictor(request):   
    if request.method == 'POST':
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
    if request.method == 'GET':
        return Response({'connected..':'Make a POST request with the required parameters to retrieve a valid response'})

@api_view(['POST','GET'])
def hepatitisPredictor(request):
    if request.method == 'POST':
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
    if request.method == 'GET':
        return Response({'connected..':'Make a POST request with the required parameters to retrieve a valid response'})

@api_view(['POST','GET'])
def strokePredictor(request):
    serializer = StrokeDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    model = ''#function .predict processed input
    return JsonResponse({'prediction':f'{model_result}'})

@api_view(['POST','GET'])
def signin(request):
    if request.method == 'POST':
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        _ , token = AuthToken.objects.create(user)

        return JsonResponse({'token':token})
    if request.method == 'GET':
        return Response({'connected..':'Make a POST request with the required parameters to retrieve a valid response'})

@api_view(['POST','GET'])
def subscribe(request):
    if request.method == 'POST':
        serializer = subscribersSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)
    if request.method == 'GET':
        return Response({'connected..':'Make a POST request with the required parameters to retrieve a valid response'})

@api_view(['POST','GET'])
@permission_classes((IsAuthenticated,))
def unsubscribe(request):
    if request.method == 'POST':
        serializer = subscribersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = subscribers.objects.filter(email=request.data["email"]).first()
            email.delete()
        except:
            return Response('you are not subscribed')
        return Response(serializer.data)
    if request.method == 'GET':
        return Response({'connected..':'Make a POST request with the required parameters to retrieve a valid response'})

@api_view(['POST','GET'])
@permission_classes((IsAuthenticated,))
def user_history(request):
    if request.method == 'POST':
        user_history_data = userHistory.objects.filter(owner=request.user)
        serializer = userHistorySerializer(user_history_data,many=True)
        return Response(serializer.data)
    if request.method == 'GET':
        return Response({'connected..':'Make a POST request with the required parameters to retrieve a valid response'})

routes = {
    'The base url' : 'http://mlclinic.herokuapp.com/api/',
    'For heart prediction' : 'http://mlclinic.herokuapp.com/api/heart/',
    'For hepatitis prediction' : 'http://mlclinic.herokuapp.com/api/hepatitis/',
    'For signup' : 'http://mlclinic.herokuapp.com/api/signup/         -[ form fields : username , password, confirm_password]',
    'For signin' : 'http://mlclinic.herokuapp.com/api/signin/         -[ form fields : username , password ]',
    'For my-history' : 'http://mlclinic.herokuapp.com/api/myhistory/  -[ send user"s token generated through successful sign-in ]',
    'For subscribe' : 'http://mlclinic.herokuapp.com/api/subscribe/   -[ form fields : email ]',
    'For unsubscribe' : 'http://mlclinic.herokuapp.com/api/unsubscribe/    -[ form fields : email ]',
    'For logout/delete token' : 'http://http://mlclinic.herokuapp.com/api/logout/   [ link the logout button directly to the link ]'
    }

@api_view(['GET'])
def connect(request):
    return Response({'API ROUTES':routes})
