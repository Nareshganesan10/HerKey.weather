from django.db import models
from django.contrib.auth.models import AbstractUser

class CityModel(models.Model):
    city_id = models.AutoField(primary_key=True, auto_created=True)
    city = models.CharField(max_length=50)
    country =  models.CharField(max_length=50)
    population = models.IntegerField()

    def __str__(self):
        return self.city
    

class CustomUser(AbstractUser):
    user_address = models.TextField()
    location_searched = models.ForeignKey(CityModel,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username