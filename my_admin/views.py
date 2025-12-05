from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from my_admin.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Customer.models import Bookings


def home(request):
    return render(request,"home.html")


def about(request):
    return render(request,"about.html")


def Booking_page(request):
    return render(request,"Booking_page.html")


def registration(request):
    if request.method == "POST":

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        mobile=request.POST.get('mobile')
        username=request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user=User.objects.create_user(username=username,email=email,password=password,first_name=full_name)
            Customer.objects.create(user=user,mobile_no=mobile,age=age,gender=gender)
            user.save()
            messages.success(request, "Registration successful! 🎉")

            return redirect("Booking_page")
        else:
            messages.error(request, "Password not match ")
            return redirect("Booking_page")

    else:
        return render(request,"Booking_page.html")



def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)

            if user.is_superuser:
                messages.success(request, "Login Successful")
                return redirect("admin_home")

            else:
                messages.success(request, "Login Successful")
                return redirect("customer_dashboard")

        else:
            messages.error(request, "Username or password is incorrect")
            return redirect("Booking_page")

    return redirect("Booking_page")


@login_required(login_url="login_view")
def admin_logout(request):
    logout(request)
    return redirect("home")


def admin_home(request):
    user=User.objects.get(id=request.user.id)

    return render(request,"main_admin.html",{'user':user})



"""--------------------Product_section--------------------------"""


def products(request):

    products=Product.objects.all()

    if request.method == "POST":
        name=request.POST.get('name')
        price=request.POST.get('price')
        description=request.POST.get('description')
        stock=request.POST.get('stock')
        available=request.POST.get('available')
        image = request.FILES.get('image')

        new_product=Product(name=name,price=price,description=description,stock=stock,available=available)
        new_product.image =image
        new_product.save()
        messages.success(request, "Product Added Successfully")
        return redirect("products")

    return render(request, 'products.html', {'products': products})



def edit_product(request,pk):
    product=Product.objects.get(id=pk)

    if request.method == "POST":

        product.name=request.POST.get('name')
        product.price=request.POST.get('price')
        product.description=request.POST.get('description')
        product.stock=request.POST.get('stock')
        product.available=request.POST.get('available')

        if 'image' in request.FILES:
            print("Hello")
            product.image = request.FILES['image']
        product.save()

        messages.info(request, "Product edited Successfully")
        return redirect('products')

    return render(request,"edit_product.html",{'product':product})



def delete_products(request,pk):
    product=Product.objects.get(id=pk)
    product.delete()
    messages.error(request, "Product Deleted Successfully")
    return redirect("products")



"""-------------------------Customer------------------------------"""

def view_customers(request):
    customers=Customer.objects.all()
    return render(request,"view_customers.html",{'customers':customers})


def delete_customer(request,pk):
    user=User.objects.get(id=pk)
    user.delete()
    messages.error(request, "Customer Deleted Successfully")
    return redirect("view_customers")



"""-------------------------Booking_order_management------------------------------"""

def customer_orders(request):
    customer_orders=Bookings.objects.all().order_by('booked_at')
    return render(request,"customer_orders.html",{"customer_orders":customer_orders})