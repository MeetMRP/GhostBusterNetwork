from django.db import models
from ghosts_and_equipments.models import *
from ghosts_and_equipments.models import Ghost,Equipment

class Mission(models.Model):
    mission_name = models.CharField(max_length=100)
    mission_date = models.DateField()
    description = models.TextField()
    encountered_ghosts = models.ManyToManyField(Ghost, blank=True, related_name='encountered_ghosts')
    equipment_used = models.ManyToManyField(Equipment, blank=True, related_name='equipment_used')
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.mission_name