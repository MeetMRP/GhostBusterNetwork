from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.RegisterApi.as_view(), name='register user'),
    path('api/email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
]
