from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Mission
from .serializers import MissionsSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *

class MissionsApi(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionsSerializers
    authentication_classes = [JWTAuthentication]

    permission_classes_by_action = {
        'create': [IsAdminUser],
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
