# booking/admin.py
from django.contrib import admin
from .models import Booking, AdminUser, SiteSettings

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'full_name', 'mobile', 'rent_date', 'status', 'paid_amount']
    list_filter = ['status', 'rent_date', 'created_at']
    search_fields = ['ticket_id', 'full_name', 'mobile', 'aadhar_number']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Personal Details', {
            'fields': ('full_name', 'aadhar_number', 'mobile', 'age', 'address', 'location')
        }),
        ('Rental Details', {
            'fields': ('hours', 'rent_date', 'rent_time')
        }),
        ('Payment Details', {
            'fields': ('total_amount', 'paid_amount', 'balance_amount', 'payment_id', 'payment_status')
        }),
        ('Status', {
            'fields': ('status', 'selfie_verified', 'terms_accepted', 'damage_policy_accepted')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_active', 'last_login']
    list_filter = ['is_active']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_phone', 'bikes_available', 'rate_per_hour']