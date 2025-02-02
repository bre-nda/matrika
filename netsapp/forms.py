from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, ShippingAddress, BillingAddress
from django.contrib.auth.forms import PasswordChangeForm

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'password']

# class UserProfileForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput,
#         required=False,
#         help_text="Leave blank to keep the current password."
#     )
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput,
#         required=False
#     )

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password and password != confirm_password:
#             raise forms.ValidationError("Passwords do not match.")
        
#         return cleaned_data
class UserProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        required=False,
        help_text="Leave blank if you don't want to change the password."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    

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
