from django.db import models
from my_admin.models import Customer, Product


class Bookings(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_bookings')
    email = models.EmailField(null=True, blank=True)
    alter_mob = models.CharField(max_length=11, null=True, blank=True)
    address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    booked_at=models.DateTimeField(auto_now_add=True)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_qty=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    payment_status = models.CharField(max_length=20,default='Pending',null=True)
    order_status = models.CharField(max_length=20,default='Pending',null=True)
    payment_method=models.CharField(max_length=11,default='None',null=True)

    def save(self, *args, **kwargs):
        if not self.notes and self.customer:
            self.notes = f"Booking by {self.customer.user.first_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.customer.user.username}"