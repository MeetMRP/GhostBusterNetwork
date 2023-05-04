from django.db import models
from location_field.models.plain import PlainLocationField

class Ghost(models.Model):
    ghost_name = models.CharField(max_length=100, primary_key=True)
    ghost_picture = models.ImageField(upload_to='ghost_picture/', blank=True)
    height = models.PositiveIntegerField(blank=True)
    weight = models.PositiveIntegerField(blank=True)
    strength = models.CharField(max_length=100, blank=True)
    weakness = models.CharField(max_length=100, blank=True)
    special_ability = models.CharField(max_length=100, blank=True)
    last_encounter_date = models.DateField(blank=True)
    last_encounter_time = models.TimeField(blank=True)
    last_encounter_place = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.ghost_name
    
class Equipment(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    use = models.TextField()
    number_of_units = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Ectoplasm(models.Model):
    location = PlainLocationField(zoom=7)
    quantity = models.PositiveIntegerField()
    belong_to = models.ForeignKey(Ghost, on_delete=models.CASCADE)

    def __str__(self):
        return "Ectoplasmic remains to " + self.belong_to.ghost_name