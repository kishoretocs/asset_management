"""
URL configuration for assect_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from user import views as user_views

# urlpatterns = [
#     path('admin/', admin.site.urls), 
#     path('register/', user_views.register, name='user-register'),
#     path('login/', auth_views.LoginView.as_view(
#         template_name='user/login.html'), name='user-login'),
#     path('profile/', user_views.profile, name='user-profile'),
#     path('profile/update/', user_views.profile_update,
#          name='user-profile-update'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'),
#          name='user-logout'),
# ]
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from user import views as user_views
from products import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='user-register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('profile/', user_views.profile, name='user-profile'),
    path('profile/update/', user_views.profile_update, name='user-profile-update'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),

    path('products/',views.products,name='product-list'),
    path('products/new/',views.create_product,name='product-create'),
    path('products/<int:pk>/edit/',views.update_product,name='product-edit'),
    path('products/<int:pk>/delete/',views.detele_product,name='product-delete'),


    path('orders/', views.order_list, name='order-list'),
    path('orders/new/', views.order_create, name='order-create'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order-edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order-delete'),

    path('user_products/', views.user_products, name='user-products'),
    path('user_products/<int:pk>/orders/', views.product_orders, name='product-orders'),
    path('user_orders/accept/<int:pk>/', views.accept_order, name='order-accept'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
]
