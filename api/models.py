from django.db import models

# Create your models here.
class Restaurant(models.Model):
    place_id = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    yelp_rating = models.FloatField(default=0)
    num_yelp_ratings = models.IntegerField(default=0)
    goog_rating = models.FloatField(default=0)
    hours = models.CharField(default="12-10", max_length= 30)
    price = models.IntegerField()


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

    def __unicode__(self):
        return str(self.name)

class GPlace(modelsModel):
    place_id = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    average_rating = models.FloatField(default=0)
    hours = models.CharField(default="12-10", max_length= 30)
    price = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.name)