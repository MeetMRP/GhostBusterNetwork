from rest_framework import serializers
from .models import *
from ghosts_and_equipments.serializers import GhostSerialisers, EquipmentSerialisers

class MissionsSerializers(serializers.ModelSerializer):
    encountered_ghosts = GhostSerialisers(many=True)
    equipment_used = EquipmentSerialisers(many=True)
    class Meta:
        model = Mission
        fields = '__all__'