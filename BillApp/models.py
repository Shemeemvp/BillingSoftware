from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    cmp_id = models.AutoField(('CID'),primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=25)
    gst_number = models.CharField(max_length=50)
    address = models.TextField()


class Items(models.Model):
    cid = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    hsn = models.IntegerField()
    unit = models.CharField(max_length=100)
    tax = models.CharField(max_length=50)
    sale_price = models.DecimalField(decimal_places=2,max_digits=8)
    purchase_price = models.DecimalField(decimal_places=2,max_digits=8)
    stock = models.IntegerField()
    date = models.DateField(auto_now_add=True, auto_now=False, null=True, blank= True)

class Item_units(models.Model):
    cid = models.ForeignKey(Company, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

class Item_transactions(models.Model):
    cid = models.ForeignKey(Company, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True, auto_now=False, blank=True, null= True)
    quantity = models.IntegerField()