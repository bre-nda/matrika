from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, ShippingAddress, BillingAddress

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'first_name', 'last_name', 'company_name', 'country', 'street_address', 'flat_suite',
            'town_city', 'state_county', 'postcode', 'phone', 'email'
        ]

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = [
            'first_name', 'last_name', 'company_name', 'country', 'street_address', 'flat_suite',
            'town_city', 'state_county', 'postcode', 'phone', 'email'
        ]
