from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Customer, Product


class CustomerInline(admin.StackedInline):
    model = Customer


class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline,)


# Unregister default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'price', 'stock')
    list_filter = ('name', 'price', 'stock')