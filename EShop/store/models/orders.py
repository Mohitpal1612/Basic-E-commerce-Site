from django.db import models
from .product import *
from .customer import *
import datetime

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField(max_length=200,blank=True)
    phone=models.CharField(max_length=10,default='')
    date=models.DateField(default=datetime.datetime.today)