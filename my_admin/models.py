from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='customer')
    mobile_no = models.CharField(max_length=11, unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=11)

    def __str__(self):
        return self.user.username



class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name} - ₹{self.price}"

