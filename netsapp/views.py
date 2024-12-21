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
    


# Mattress Views
    
def mattress_page(request):
    mattresses = Mattress.objects.all()
    return render(request, 'mattress.html', {'mattresses': mattresses})

def quilted_mattress_page(request):
    quilted_mattresses = Mattress.objects.filter(type='quilted')  # Filter for quilted mattresses
    return render(request, 'quilted.html', {'quilted_mattresses': quilted_mattresses})

def plain_mattress_page(request):
    plain_mattresses = Mattress.objects.filter(type='plain')  #Filter for plain mattresses
    return render(request, 'plain.html', {'plain_mattresses': plain_mattresses})

def mattress_detail(request, type, thickness):
    # Filter the mattress based on type and thickness
    mattresses = Mattress.objects.filter(type=type, thickness=thickness)

    return render(request, 'mattress_detail.html', {
        'mattresses': mattresses,
        'type': type,
        'thickness': thickness,
    })



# Bedding views

def bedding_page(request):
    bedsheets = Bedsheet.objects.all()
    duvets = Duvet.objects.all()
    pillows = Pillow.objects.all()
    return render(request, 'bedding.html', {
        'bedsheets': bedsheets,
        'duvets': duvets,
        'pillows': pillows,
    })