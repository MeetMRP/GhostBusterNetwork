from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.RegisterApi.as_view(), name='register user'),
    path('api/login/', views.LoginApi.as_view(), name='login user'),
    path('api/email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
]
