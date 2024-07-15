from user.models import Profile
from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    category = models.CharField(max_length=50, null=True)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products',null=True, blank=True,default=1)

    def __str__(self):
        return self.name



class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    order_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivered = models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.product.sell_price * self.order_quantity
        super().save(*args, **kwargs)

    def __str__(self):
       return f'Order of {self.product.name} by {self.customer.customer.username}'
