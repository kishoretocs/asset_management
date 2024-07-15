from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Order
from .forms import ProductForm,OrderForm
from user.models import Profile
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html',{'form':form})

def update_product(reqeust,pk):
    product = get_object_or_404(Product, pk=pk)
    if reqeust.method == 'POST':
        form =  ProductForm(reqeust.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    return render(reqeust,'products/product_form.html',{'form':form})

def products(request):
    products = Product.objects.all()
    return render(request,'products/product_list.html',{'products':products})

def detele_product(reqeust,pk):
    product = get_object_or_404(Product,id=pk)
    if reqeust.method == 'POST':
        product.delete()
        return redirect( 'product-list')
    return render(reqeust,'products/product_confirm_delete.html',{'product':product})



@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = Profile.objects.get(customer=request.user)
            order.save()
            return redirect('order-list')
    else:
        form = OrderForm()
    return render(request, 'order/order_form.html', {'form': form})

@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk, customer__customer=request.user)
    if request.method == 'POST':
        order.delete()
        return redirect('order-list')
    return render(request, 'order/order_confirm_delete.html', {'order': order})


@login_required
def order_list(request):
    user_profile = Profile.objects.get(customer=request.user)
    orders = Order.objects.filter(customer=user_profile)
    return render(request, 'order/order_list.html', {'orders': orders})

# Edit an order
@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk,  customer__customer=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order-list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'order/order_form.html', {'form': form})


@login_required
def user_products(request):
    profile = Profile.objects.get(customer=request.user)
    products = Product.objects.filter(creator=profile)
    return render(request, 'products/user_product.html', {'products': products})


@login_required
def product_orders(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.creator != Profile.objects.get(customer=request.user):
        return redirect('user-products')  # or raise an Http404 exception

    orders = Order.objects.filter(product=product, delivered=False)
    return render(request, 'products/product_order.html', {'product': product, 'orders': orders})



# views.py
@login_required
def accept_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    product = order.product

    # Ensure the logged-in user is the creator of the product
    if product.creator != Profile.objects.get(customer=request.user):
        return redirect('product-orders', pk=product.pk)  # or raise an Http404 exception

    if request.method == 'POST':
        if order.order_quantity <= product.quantity:
            product.quantity -= order.order_quantity
            product.save()
            order.delivered = True
            order.save()
            messages.success(request, 'Order has been accepted and processed successfully.')
            return redirect('product-orders', pk=product.pk)
        else:
            return render(request, 'order/accept_order.html', {'order': order, 'error': 'Not enough stock available.'})

    return render(request, 'order/accept_order.html', {'order': order})



@login_required
def dashboard_view(request):
    profile = Profile.objects.get(customer=request.user)

    # Fetching and serializing data
    products = list(Product.objects.filter(creator=profile).values('id', 'name', 'quantity', 'sell_price'))
    orders = list(Order.objects.filter(product__creator=profile).values('id', 'product__name', 'order_quantity', 'total_price', 'order_date','delivered'))
    
    sales_count = Order.objects.filter(product__creator=profile).count()
    total_revenue = Order.objects.filter(product__creator=profile).aggregate(Sum('product__sell_price'))['product__sell_price__sum']
    customer_count = Order.objects.filter(product__creator=profile).values('customer').distinct().count()

    delivered_orders_count = Order.objects.filter(product__creator=profile, delivered=True).count()
    not_delivered_orders_count = Order.objects.filter(product__creator=profile, delivered=False).count()

    context = {
        'profile': {
            'username': profile.customer.username,
            'email': profile.email,
            'phone': profile.phone,
            'address': profile.address,
        },
        'products': products,
        'orders': orders,
        'sales_count': sales_count,
        'total_revenue': float(total_revenue) if total_revenue else 0,
        'customer_count': customer_count,
        'delivered_orders_count': delivered_orders_count,
        'not_delivered_orders_count': not_delivered_orders_count,

    }

    return JsonResponse(context)



# @login_required
# def dashboard_view(request):
#     profile = Profile.objects.get(customer=request.user)
    
#     # Example data fetching
#     sales_count = Order.objects.filter(product__creator=profile).count()
#     total_revenue = Order.objects.filter(product__creator=profile).aggregate(Sum('product__sell_price'))['product__sell_price__sum']
#     customer_count = Order.objects.filter(product__creator=profile).values('customer').distinct().count()
    
#     context = {
#         'profile': profile,
#         'sales_count': sales_count,
#         'total_revenue': total_revenue if total_revenue else 0,
#         'customer_count': customer_count,
#     }
    
#     return render(request, 'order/dashboard.html', context)
