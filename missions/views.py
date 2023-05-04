from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Mission
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
import json
from urllib.request import urlopen
from django.core.mail import EmailMessage
from accounts.models import user

class MissionsApi(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionsSerializers
    authentication_classes = [JWTAuthentication]

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
        
class PickleApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_user = request.user

        response = urlopen('http://ipinfo.io/json')
        response = json.load(response) #user ip info

        #email sending
        email_subject = 'Code PICKLE'
        email_body = f"User: {request_user.f_name} {request_user.l_name} ({request_user.username}) is encountering an emergency.\nUser's locations is {response['city']}, {response['region']}, {response['country']}({response['loc']})\nIP address: {response['ip']}\n\n\n(NOTE:This is a system generated mail do not reply to it.)"
        Staffs = user.objects.filter(is_staff = True)
        email_receivers = []
        for staff in Staffs:
            email_receivers.append(staff.email)
        email = EmailMessage(
                subject=email_subject, 
                body=email_body, 
                to=email_receivers
                )
        email.send()
        
        return Response({'Message':'An emergency message has ben sent to each staff member alerting about you location'}, status=status.HTTP_200_OK)
