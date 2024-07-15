from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Order
from user.models import Profile

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)