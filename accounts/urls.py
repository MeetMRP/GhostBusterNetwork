from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    #refresh token endpoint
    path('api/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('api/register/', views.RegisterApi.as_view(), name='register user'),
    path('api/login/', views.LoginApi.as_view(), name='login user'),
    path('api/email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
    path('api/passowrd-reset-email/', views.RequestPasswordResetEmail.as_view(), name='passowrd-reset'),
    path('api/passowrd-reset-check/<uidb64>/<token>/', views.PasswordTokenCheckApi.as_view(), name='passowrd-reset-check'),
    path('api/passowrd-reset-complete/', views.SetNewPassowrdApi.as_view(), name='passowrd-reset-complete'),
]
