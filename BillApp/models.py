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