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
    user_city = models.TextField()
    

class SearchModel(models.Model):
    location_searched = models.TextField(null=True)
    username = models.CharField(max_length=50, null=False)
    searched_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username, self.location_searched, self.searched_at