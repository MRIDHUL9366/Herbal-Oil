from django.urls import path
from . import views


urlpatterns = [

    path("", views.customer_dashboard, name='customer_dashboard'),
    path("logout_customer/", views.logout_customer, name='logout_customer'),
    #-----------------Booking--------------------------------------#
    path('book_product/<int:pk>', views.book_product, name='book_product'),
    path('booking_confirmation', views.booking_confirmation, name='booking_confirmation'),
    path('booking_payment', views.booking_payment, name='booking_payment'),
    path('booking_razorpay_payment', views.booking_razorpay_payment, name='booking_razorpay_payment'),
    path('my_bookings', views.my_bookings, name='my_bookings'),
    path('booking_product_view/<int:pk>', views.booking_product_view, name='booking_product_view'),

]