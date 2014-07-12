from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    average_rating = models.FloatField(default=0)
    num_ratings = models.IntegerField(default=0)
    hours = models.CharField(default="12-10", max_length= 30)


class Yelp(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    average_rating = models.FloatField(default=0)
    num_ratings = models.IntegerField(default=0)
    hours = models.CharField(default="12-10", max_length= 30)