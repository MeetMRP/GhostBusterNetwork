from rest_framework import serializers
from .models import *
from ghosts_and_equipments.models import *

class MissionsSerializers(serializers.ModelSerializer):
    encountered_ghosts = serializers.PrimaryKeyRelatedField(many=True, queryset=Ghost.objects.all())
    equipment_used = serializers.PrimaryKeyRelatedField(many=True, queryset=Equipment.objects.all())
    class Meta:
        model = Mission
        fields = '__all__'