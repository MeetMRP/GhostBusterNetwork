from rest_framework import serializers
from .models import *

class GhostSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Ghost
        fields = '__all__'

class EquipmentSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class EctoplasmSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Ectoplasm
        fields = '__all__'