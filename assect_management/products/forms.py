from .models import Product,Order
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'category', 'description', 'cost', 'sell_price']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =['product','order_quantity']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']