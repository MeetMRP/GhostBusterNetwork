from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, login, logout

class RegisterApi(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) #will give error msg when something goes wrong
        serializer.save()
        user_data = serializer.data #user's data

        #generating the abosulte url
        current_site = get_current_site(request).domain
        url_path = reverse('email-verify')
        request_user = user.objects.get(username=user_data['username'])
        token = RefreshToken.for_user(request_user).access_token
        abs_url = 'http//' + current_site + url_path + '?token=' + str(token) 

        #email sending
        email_subject = 'Email verification.'
        email_body = f'Hi {request_user.f_name} {request_user.l_name} ({request_user.username})\nUse the link below to verify yourself.\n {abs_url}\n\n(NOTE:This is a system generated mail do not reply to it.)'
        email_receiver = request_user.email
        email = EmailMessage(
                subject=email_subject, 
                body=email_body, 
                to=[email_receiver]
                )
        email.send()

        user_data['message'] = 'Check email to verify yourself'
        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    #added token query for swagger docs
    token_param_config = openapi.Parameter(name='token', in_=openapi.IN_QUERY, description='Enter the access token', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            request_user = user.objects.get(id = payload['user_id'])
            if request_user.is_verified == False:
                request_user.is_verified = True
                request_user.save()
            return Response({'Email':'Successfully verified'}, status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError:
            return Response({'error':'Access Token expired get another one'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError:
            return Response({'error':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginApi(GenericAPIView):
    serializer_class=LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)