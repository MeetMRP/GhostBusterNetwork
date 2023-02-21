from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
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
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 


#new user registration
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
        email_body = f'Hi, {request_user.f_name} {request_user.l_name} ({request_user.username})\nUse the link below to verify yourself.\n {abs_url}\n\n(NOTE:This is a system generated mail do not reply to it.)'
        email_receiver = request_user.email
        email = EmailMessage(
                subject=email_subject, 
                body=email_body, 
                to=[email_receiver]
                )
        email.send()

        user_data['message'] = 'Check email to verify yourself'
        return Response(user_data, status=status.HTTP_201_CREATED)


#email verification
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
        

#existing user login
class LoginApi(GenericAPIView):
    serializer_class=LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

#Sending an email to request password reset 
class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializers

    def post(self, request):
        data = {
            'request': request,
            'data': request.data
        }
        serializer = self.get_serializer(data=data)
        email = request.data['email']
        print(email)
        if user.objects.filter(email=email).exists():
            request_user = user.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(request_user.id))
            token = PasswordResetTokenGenerator().make_token(request_user)

            #generating the abosulte url
            current_site = get_current_site(request).domain
            url_path = reverse('passowrd-reset-check', kwargs={'uidb64': uidb64, 'token': token})
            abs_url = 'http//' + current_site + url_path
            
            #email sending
            email_subject = 'Password reset.'
            email_body = f'Hi, {request_user.f_name} {request_user.l_name} ({request_user.username})\nUse the link below to reset your password.\n {abs_url}\n\n(NOTE:This is a system generated mail do not reply to it.)'
            email_receiver = request_user.email
            email = EmailMessage(
                    subject=email_subject, 
                    body=email_body, 
                    to=[email_receiver]
                    )
            email.send()
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


#Check if user exists also check token and uidb64
class PasswordTokenCheckApi(GenericAPIView):
    serializer_class = []
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            request_user = user.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(request_user, token):
                return Response({'error': 'Token is not valid, please request a new one'})
            
            return Response({'success': True, 'message': 'Valid Credentials', 'uidb64': uidb64, 'token': token})
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Connot decode the token, please request a new one'})


#set new password
class SetNewPassowrdApi(GenericAPIView):
    serializer_class = SetNewPassowrdApiSerializer

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password Reset successfull'}, status=status.HTTP_200_OK)