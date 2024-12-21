from django.contrib import admin
from .models import Bedsheet, Duvet, Mattress, Pillow

# Register your models here.

admin.site.register(Mattress)
admin.site.register(Duvet)
admin.site.register(Bedsheet)
admin.site.register(Pillow)
