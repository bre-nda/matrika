from django.contrib import admin
from .models import Bedsheet, Duvet, Mattress, Pillow, CartItem, UserProfile, ShippingAddress, BillingAddress, Order, OrderItem

# Register your models here.

admin.site.register(Mattress)
admin.site.register(Duvet)
admin.site.register(Bedsheet)
admin.site.register(Pillow)
admin.site.register(CartItem)
admin.site.register(UserProfile)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
