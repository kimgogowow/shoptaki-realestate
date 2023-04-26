from django.db import models
from datetime import datetime

# Create your models here.



class Listing(models.Model):
    address = models.CharField(max_length=200, default = "5000 Forbes Ave")
    city = models.CharField(max_length=100, default="Pittsburgh")
    state = models.CharField(max_length=100, default="PA")
    zipcode = models.CharField(max_length=20, default=-1)
    price = models.DecimalField(max_digits=30, decimal_places=2, default =-1)
    bedrooms = models.IntegerField(default=-1)
    bathrooms = models.DecimalField(max_digits=7, decimal_places=2, default=-1)
    sqft = models.DecimalField(max_digits=20, decimal_places=2, default =-1)
    lot_size = models.DecimalField(max_digits=20, decimal_places=2, default =-1)
    days_listed = models.IntegerField(default=-1)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, default=-1)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, default=-1)
    img = models.CharField(max_length=200, default="")
    rent_estimate = models.DecimalField(max_digits=30, decimal_places=5, default =-1)

    def __str__(self):
        return self.title


class Analytics(models.Model):
    cap_rate = models.IntegerField()
    loan_to_value = models.IntegerField()
    current_savings = models.IntegerField()
    interest_rate = models.IntegerField()
    amort_sched = models.IntegerField()
    def __str__(self):
        return self.title

class ListingAnalytics(models.Model):
    noi = models.DecimalField(max_digits=10, decimal_places=2, default=-1)
    monthly_noi = models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    p_interest = models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    p_fcf= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    p_cashoncash= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    p_debtyield= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    p_debtconstant= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    pandi_principal= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    pandi_interest= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    pandi_fcf= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    pandi_cashoncash= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    pandi_debtyield= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    pandi_debtconstant= models.DecimalField(max_digits=12, decimal_places=2, default=-1)
    def __str__(self):
        return self.title