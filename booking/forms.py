# booking/forms.py
from django import forms
from .models import Booking
import re

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'full_name', 'aadhar_number', 'mobile', 'age', 
            'address', 'location', 'hours', 'rent_date', 'rent_time'
        ]
        widgets = {
            'rent_date': forms.DateInput(attrs={'type': 'date'}),
            'rent_time': forms.TimeInput(attrs={'type': 'time'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'location': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Share location or type manually'}),
        }
    
    def clean_aadhar_number(self):
        aadhar = self.cleaned_data['aadhar_number']
        # Remove spaces and check length
        cleaned = re.sub(r'\s', '', aadhar)
        if not re.match(r'^\d{12}$', cleaned):
            raise forms.ValidationError('Invalid Aadhar number format')
        return aadhar
    
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not re.match(r'^\d{10}$', mobile):
            raise forms.ValidationError('Mobile number must be 10 digits')
        return mobile
    
    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise forms.ValidationError('Age must be 18 or above')
        return age

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class TicketSearchForm(forms.Form):
    ticket_id = forms.CharField(max_length=20, required=False)
    mobile = forms.CharField(max_length=10, required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        ticket_id = cleaned_data.get('ticket_id')
        mobile = cleaned_data.get('mobile')
        
        if not ticket_id and not mobile:
            raise forms.ValidationError('Please enter either Ticket ID or Mobile number')
        
        return cleaned_data