# booking/admin_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
import hashlib
from .models import Booking, AdminUser, SiteSettings
from .forms import AdminLoginForm
from .decorators import admin_login_required, prevent_cache

def admin_login(request):
    """Custom admin login"""
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check against settings
            if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
                request.session['admin_logged_in'] = True
                request.session['admin_username'] = username
                request.session['admin_login_time'] = timezone.now().isoformat()
                messages.success(request, 'Login successful!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin/admin_login.html', {'form': form})

def admin_logout(request):
    """Admin logout"""
    request.session.pop('admin_logged_in', None)
    request.session.pop('admin_username', None)
    messages.success(request, 'Logged out successfully')
    return redirect('admin_login')

@admin_login_required
@prevent_cache
def admin_dashboard(request):
    """Admin dashboard"""
    # Get statistics
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    
    # Revenue
    total_revenue = sum(b.paid_amount or 0 for b in Booking.objects.all())
    today_revenue = sum(
        b.paid_amount or 0 
        for b in Booking.objects.filter(created_at__date=timezone.now().date())
    )
    
    # Recent bookings
    recent_bookings = Booking.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'recent_bookings': recent_bookings,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin/admin_dashboard.html', context)

@admin_login_required
def booking_list(request):
    """List all bookings with filters"""
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    
    bookings = Booking.objects.all()
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    if date_filter:
        bookings = bookings.filter(rent_date=date_filter)
    
    context = {
        'bookings': bookings.order_by('-created_at'),
        'status_filter': status_filter,
        'date_filter': date_filter,
    }
    
    return render(request, 'admin/bookings_list.html', context)

@admin_login_required
def booking_detail(request, booking_id):
    """View and update booking details"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in dict(Booking.STATUS_CHOICES):
                booking.status = new_status
                booking.save()
                messages.success(request, f'Booking status updated to {new_status}')
        
        elif action == 'update_payment':
            booking.payment_status = request.POST.get('payment_status', booking.payment_status)
            booking.save()
            messages.success(request, 'Payment status updated')
        
        return redirect('booking_detail', booking_id=booking.id)
    
    return render(request, 'admin/booking_detail.html', {'booking': booking})

@admin_login_required
def get_booking_stats(request):
    """Get booking statistics for dashboard charts"""
    import json
    from django.db.models import Count
    from django.db.models.functions import TruncDate
    
    # Daily bookings for last 7 days
    daily_bookings = Booking.objects.filter(
        created_at__gte=timezone.now() - timezone.timedelta(days=7)
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Status distribution
    status_counts = Booking.objects.values('status').annotate(count=Count('id'))
    
    data = {
        'daily_bookings': list(daily_bookings),
        'status_counts': list(status_counts),
    }
    
    return JsonResponse(data)