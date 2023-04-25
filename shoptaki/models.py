from django.db import models
from datetime import datetime

# Create your models here.



class Listing(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    days_listed = models.IntegerField()
    longitude = models.DecimalField()
    latitude = models.DecimalField()
    img = models.CharField(max_length=200)
    rent_estimate = models.IntegerField()

    def __str__(self):
        return self.title