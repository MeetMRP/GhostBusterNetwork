from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Mission
from .serializers import MissionsSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from django_filters.rest_framework import DjangoFilterBackend

class MissionsApi(ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionsSerializers
    authentication_classes = [JWTAuthentication]
    filter_backends = (DjangoFilterBackend,)
    filter_fields=('encountered_ghosts','equipment_used')

    permission_classes_by_action = {
        'create': [AllowAny],
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
