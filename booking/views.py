# booking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import json
import base64
from django.core.files.base import ContentFile
from .models import Booking, SiteSettings
from .forms import BookingForm, TicketSearchForm
from .utils import create_razorpay_order, verify_payment_signature, generate_receipt_text
from .decorators import prevent_cache
import razorpay

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def home(request):
    """Home page view"""
    context = {
        'site_settings': SiteSettings.objects.first(),
        'recent_bookings': Booking.objects.filter(status='confirmed')[:5]
    }
    return render(request, 'home.html', context)

def booking_view(request):
    """Booking form page (Stage 1)"""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save form data in session
            booking_data = form.cleaned_data
            request.session['booking_data'] = {
                k: (v.isoformat() if hasattr(v, 'isoformat') else v)
                for k, v in booking_data.items()
            }
            messages.success(request, 'Details verified! Please proceed with selfie')
            return redirect('selfie')
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {'form': form})

def selfie_view(request):
    """Selfie verification page (Stage 2)"""
    if 'booking_data' not in request.session:
        messages.error(request, 'Please fill booking details first')
        return redirect('book')
    
    if request.method == 'POST':
        selfie_data = request.POST.get('selfie_image')
        if selfie_data:
            # Save selfie temporarily
            format, imgstr = selfie_data.split(';base64,')
            ext = format.split('/')[-1]
            selfie_file = ContentFile(
                base64.b64decode(imgstr), 
                name=f"selfie_{timezone.now().timestamp()}.{ext}"
            )
            
            # Store in session (just the name for now)
            request.session['selfie_verified'] = True
            messages.success(request, 'Selfie captured successfully!')
            return redirect('terms')
    
    return render(request, 'selfie.html')

def terms_view(request):
    """Terms and conditions page (Stage 3)"""
    if 'booking_data' not in request.session:
        return redirect('book')
    
    if request.method == 'POST':
        terms_accepted = request.POST.get('terms') == 'on'
        damage_accepted = request.POST.get('damage_policy') == 'on'
        
        if terms_accepted and damage_accepted:
            request.session['terms_accepted'] = True
            request.session['damage_accepted'] = True
            return redirect('payment')
        else:
            messages.error(request, 'Please accept all terms to proceed')
    
    return render(request, 'terms.html')

def payment_view(request):
    """Payment page (Stage 4)"""
    if not all(k in request.session for k in ['booking_data', 'selfie_verified', 'terms_accepted']):
        messages.error(request, 'Please complete all previous steps')
        return redirect('book')
    
    booking_data = request.session.get('booking_data', {})
    hours = int(booking_data.get('hours', 2))
    total_amount = hours * 200
    paid_amount = 50
    balance_amount = total_amount - 50
    
    # Create Razorpay order
    order = create_razorpay_order(paid_amount, f"booking_{timezone.now().timestamp()}")
    
    if order:
        request.session['razorpay_order_id'] = order['id']
    
    context = {
        'booking_data': booking_data,
        'total_amount': total_amount,
        'paid_amount': paid_amount,
        'balance_amount': balance_amount,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'order': order,
        'hours': hours
    }
    
    return render(request, 'payment.html', context)

@csrf_exempt
def payment_callback(request):
    """Handle payment success callback from Razorpay"""
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        
        # Verify signature
        if verify_payment_signature(order_id, payment_id, signature):
            # Get data from session
            booking_data = request.session.get('booking_data', {})
            
            # Create booking
            booking = Booking.objects.create(
                full_name=booking_data.get('full_name'),
                aadhar_number=booking_data.get('aadhar_number'),
                mobile=booking_data.get('mobile'),
                age=booking_data.get('age'),
                address=booking_data.get('address'),
                location=booking_data.get('location'),
                hours=booking_data.get('hours'),
                rent_date=booking_data.get('rent_date'),
                rent_time=booking_data.get('rent_time'),
                payment_id=payment_id,
                order_id=order_id,
                payment_signature=signature,
                payment_status='completed',
                status='confirmed',
                terms_accepted=request.session.get('terms_accepted', False),
                damage_policy_accepted=request.session.get('damage_accepted', False),
            )
            
            # Clear session
            for key in ['booking_data', 'selfie_verified', 'terms_accepted', 'damage_accepted', 'razorpay_order_id']:
                request.session.pop(key, None)
            
            # Store booking ID for receipt
            request.session['last_booking_id'] = booking.id
            
            return JsonResponse({'status': 'success', 'booking_id': booking.id})
        else:
            return JsonResponse({'status': 'failed', 'error': 'Invalid signature'})
    
    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})

def receipt_view(request, booking_id=None):
    """Receipt page (Stage 5)"""
    if not booking_id:
        booking_id = request.session.get('last_booking_id')
    
    if not booking_id:
        messages.error(request, 'No booking found')
        return redirect('home')
    
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'receipt.html', {'booking': booking})

def download_receipt(request, booking_id):
    """Download receipt as text file"""
    booking = get_object_or_404(Booking, id=booking_id)
    receipt_text = generate_receipt_text(booking)
    
    response = HttpResponse(receipt_text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="SkyBicycle_{booking.ticket_id}.txt"'
    return response

def search_booking(request):
    """Search for a booking by ticket ID or mobile"""
    if request.method == 'POST':
        form = TicketSearchForm(request.POST)
        if form.is_valid():
            ticket_id = form.cleaned_data['ticket_id']
            mobile = form.cleaned_data['mobile']
            
            if ticket_id:
                bookings = Booking.objects.filter(ticket_id__icontains=ticket_id)
            else:
                bookings = Booking.objects.filter(mobile=mobile)
            
            return render(request, 'search_results.html', {'bookings': bookings, 'form': form})
    else:
        form = TicketSearchForm()
    
    return render(request, 'search_booking.html', {'form': form})

def my_bookings(request):
    """View bookings by mobile number"""
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        if mobile:
            bookings = Booking.objects.filter(mobile=mobile).order_by('-created_at')
            return render(request, 'my_bookings.html', {'bookings': bookings, 'mobile': mobile})
    
    return render(request, 'my_bookings.html')