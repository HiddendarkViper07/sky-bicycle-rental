# booking/models.py
from django.db import models
from django.utils import timezone
import uuid
import random

def generate_ticket_id():
    """Generate unique ticket ID like SKY-1234"""
    return f"SKY-{random.randint(1000, 9999)}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Personal Details
    ticket_id = models.CharField(max_length=20, unique=True, default=generate_ticket_id)
    full_name = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    age = models.IntegerField()
    address = models.TextField()
    location = models.TextField(help_text="Location coordinates or address")
    
    # Rental Details
    hours = models.IntegerField(default=2)
    rent_date = models.DateField()
    rent_time = models.TimeField()
    
    # Selfie Image
    selfie = models.ImageField(upload_to='selfies/', null=True, blank=True)
    selfie_verified = models.BooleanField(default=False)
    
    # Payment Details
    total_amount = models.IntegerField(default=0)
    paid_amount = models.IntegerField(default=0)
    balance_amount = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_signature = models.TextField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='pending')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Terms
    terms_accepted = models.BooleanField(default=False)
    damage_policy_accepted = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.ticket_id} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.hours * 200
            self.paid_amount = 50
            self.balance_amount = self.total_amount - 50
        super().save(*args, **kwargs)

class AdminUser(models.Model):
    """Custom admin user for the panel"""
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # Will store hashed password
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.username

class SiteSettings(models.Model):
    """Site configuration settings"""
    site_name = models.CharField(max_length=100, default='Sky Bicycle Rental')
    contact_phone = models.CharField(max_length=15, default='+919876543210')
    contact_email = models.EmailField(default='ride@skybicycle.in')
    address = models.TextField(default='Downtown Hub')
    bikes_available = models.IntegerField(default=6)
    rate_per_hour = models.IntegerField(default=200)
    booking_amount = models.IntegerField(default=50)
    
    class Meta:
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name