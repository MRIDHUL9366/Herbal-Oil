from django.shortcuts import render
from django.http import HttpResponse




def customer_dashboard(request):
    return render(request,'customer_dashboard.html')
