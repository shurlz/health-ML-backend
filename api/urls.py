from django.urls import path
from . import views
from knox import views as knox_views

urlpatterns = [
    path('', views.heartPredictor ,name='get_prediction'),
    path('signup/', views.signup ,name='signup'),
    path('logout/', knox_views.LogoutAllView.as_view() ,name='logout'),
    path('signin/', views.signin ,name='signin'),

    path('hepatitis/', views.hepatitisPredictor ,name='hepatitis'),
    path('heart/', views.heartPredictor ,name='heart'),
    path('stroke/', views.strokePredictor ,name='stroke'),

    path('subscribe/', views.subscribe ,name='subscribe'),
    path('unsubscribe/', views.unsubscribe ,name='unsubscribe'),
    path('myhistory/', views.user_history , name='myhistory')
]


