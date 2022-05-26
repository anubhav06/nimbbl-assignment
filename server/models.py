from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"


class Product(models.Model):

    name = models.CharField(max_length=64)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.price}"
