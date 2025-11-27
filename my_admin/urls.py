from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('Booking_page',views.Booking_page,name='Booking_page'),
    path('registration',views.registration,name='registration'),
    path('login_view', views.login_view, name='login_view'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),
    #-------------------Products----------------------------#
    path('products', views.products, name='products'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete_products/<int:pk>/', views.delete_products, name='delete_products'),
    #-------------------Customer-----------------------------------#
    path('view_customers', views.view_customers, name='view_customers'),
    path('delete_customer/<int:pk>/', views.delete_customer, name='delete_customer'),
    # ----------------------------Booking--------------------------------------
    path('customer_orders', views.customer_orders, name='customer_orders'),

]
