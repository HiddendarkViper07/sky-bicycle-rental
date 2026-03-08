# booking/urls.py (User URLs)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.booking_view, name='book'),
    path('selfie/', views.selfie_view, name='selfie'),
    path('terms/', views.terms_view, name='terms'),
    path('payment/', views.payment_view, name='payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    path('receipt/<int:booking_id>/', views.receipt_view, name='receipt'),
    path('download-receipt/<int:booking_id>/', views.download_receipt, name='download_receipt'),
    path('search/', views.search_booking, name='search_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]