from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from my_admin.models import Product,Customer
from .models import Bookings
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail



def customer_dashboard(request):
    user=User.objects.get(id=request.user.id)
    product=Product.objects.get(id=1)
    context = {
        'user': user,
        'product': product,
    }
    return render(request,'customer_dashboard.html',context)



def logout_customer(request):
    return redirect('home')

"""---------------------Bookings------------------"""

def book_product(request,pk):
    request.session['product'] = pk
    product=Product.objects.get(id=pk)
    user=User.objects.get(id=request.user.id)
    context = {
        'product': product,
        'user': user,
    }
    return render(request,'book_product.html', context)



def booking_confirmation(request):

    if request.method == "POST":
        custName = request.POST.get('custName')
        custEmail = request.POST.get('custEmail')
        custPhone = request.POST.get('custPhone')
        addPhone = request.POST.get('addPhone')
        custAddress = request.POST.get('custAddress')
        qty = request.POST.get('qty')
        total = request.POST.get('totalPrice')
        notes = request.POST.get('notes')

        request.session['booking_data'] = {

            'custName': custName,
            'custEmail': custEmail,
            'custPhone': custPhone,
            'addPhone': addPhone,
            'custAddress': custAddress,
            'qty': qty,
            'total': total,
            'notes': notes,
        }

        # Redirect to payment page
        return redirect('booking_payment')
    try:
        product = Product.objects.get(id=request.session['product'])
        user = User.objects.get(id=request.user.id)
        booking_data = request.session.get('booking_data')

        context={
            'product':product,
            'user':user,
            'booking_data':booking_data,
        }
        return render(request, 'book_product.html',context )
    except Exception as e:
        print(e)
        return redirect('book_product')




def booking_details_save(request, payment_method, booking_data):
    customer = Customer.objects.get(user_id=request.user.id)
    product = Product.objects.get(id=request.session['product'])

    # Create booking entry
    booking = Bookings.objects.create(
        customer=customer,
        email=booking_data['custEmail'],
        alter_mob=booking_data['addPhone'],
        address=booking_data['custAddress'],
        total_amount=booking_data['total'],
        total_qty=booking_data['qty'],
        notes=booking_data['notes'],
        payment_status="Success",
        order_status="Confirmed",
        payment_method=payment_method,
        product=product
    )
    send_mail(
        subject="Booking Confirmation – Thank You!",
        message=f"""
    Dear {customer.user.first_name},

    Thank you for your booking with us!

    Your order has been successfully confirmed.  
    Below are your booking details:

    • Total Quantity   : {booking_data['qty']}
    • Total Amount     : ₹{booking_data['total']}
    • Payment Status   : Success  
    • Order Status     : Confirmed  

    We truly appreciate your trust in us.  
    If you have any questions or need support, please feel free to contact us.

    Warm regards,  
   Himalaya herbal oil
    """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[booking_data['custEmail']],
        fail_silently=False,
    )

    # Remove session data
    if 'booking_data' in request.session:
        del request.session['booking_data']

    messages.success(request, "Payment successfully processed!")
    return redirect('my_bookings')



@never_cache
def booking_payment(request):
    booking_data = request.session.get('booking_data')

    if not booking_data:
        return redirect('customer_dashboard')

    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        return booking_details_save(request, payment_method, booking_data)


    return render(request, "booking_payment.html", {"booking_data": booking_data})


@never_cache
def booking_razorpay_payment(request):
    booking_data = request.session.get('booking_data')
    if not booking_data:
        return redirect('customer_dashboard')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    amount = int(float(booking_data['total']) * 100)

    order = client.order.create(dict(amount=amount, currency="INR", payment_capture=1))

    return render(request, "razor_pay.html", {
        'order_id': order['id'],
        'amount': booking_data['total'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'booking_data': booking_data,
        'payment_method': 'card'
    })



def my_bookings(request):
    customer=Customer.objects.get(user_id=request.user.id)
    my_bookings = Bookings.objects.filter(customer=customer).order_by('-booked_at')
    return render(request, 'my_bookings.html',{"my_bookings":my_bookings})



def booking_product_view(request, pk):
    product=Product.objects.get(id=pk)
    return render(request, 'booking_product_view.html',{"product":product})




