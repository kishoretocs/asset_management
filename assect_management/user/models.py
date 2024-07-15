from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    customer = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField(max_length=200,blank=True,null=True)

    def __str__(self):
        return f'{self.customer.username}-Profile'