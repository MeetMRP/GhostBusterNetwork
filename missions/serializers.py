from rest_framework import serializers
from .models import *
from ghosts_and_equipments.serializers import GhostSerialisers, EquipmentSerialisers

class MissionsSerializers(serializers.ModelSerializer):
    encountered_ghosts = serializers.SlugRelatedField(queryset=Ghost.objects.all(), slug_field='ghost_name')
    equipment_used = serializers.SlugRelatedField(queryset=Equipment.objects.all(), slug_field='name')
    class Meta:
        model = Mission
        fields = ['mission_name', 'mission_date', 'description', 'encountered_ghosts', 'equipment_used', 'is_complete']

    def save(self):
        encountered_ghosts =self.validated_data['encountered_ghosts']
        equipment_used = self.validated_data['equipment_used']
        report = Mission(
            mission_name=self.validated_data['mission_name'],
            mission_date=self.validated_data['mission_date'],
            description=self.validated_data['description'],
            is_complete=self.validated_data['is_complete'],
        )
        report.save()
        report.encountered_ghosts.set([encountered_ghosts])
        report.equipment_used.set([equipment_used])
        report.save()