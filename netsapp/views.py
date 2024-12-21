from django.shortcuts import render
from .models import Mattress, Duvet, Bedsheet, Pillow

# Create your views here.

# def Home(request):
#     return render(request, 'index.html')

def Home(request):
    mattresses = Mattress.objects.all()
    duvets = Duvet.objects.all()
    bedsheets = Bedsheet.objects.all()
    pillows = Pillow.objects.all()
    
    return render(request, 'index.html', {
        'mattresses': mattresses,
        'duvets': duvets,
        'bedsheets': bedsheets,
        'pillows': pillows
    })