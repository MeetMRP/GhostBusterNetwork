from django.db import models
from ghosts_and_equipments.models import *
from ghosts_and_equipments.models import Ghost,Equipment

class Mission(models.Model):
    mission_name = models.CharField(max_length=100)
    mission_date = models.DateField()
    description = models.TextField()
    encountered_ghosts = models.ManyToManyField(Ghost, blank=True)
    equipment_used = models.ManyToManyField(Equipment, blank=True)
    is_complete = models.BooleanField()

    def __str__(self):
        return self.mission_name