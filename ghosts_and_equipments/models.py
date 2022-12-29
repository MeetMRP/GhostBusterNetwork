from django.db import models

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

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    use = models.TextField()
    number_of_units = models.PositiveIntegerField()