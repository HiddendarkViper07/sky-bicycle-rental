# booking/admin_urls.py (Admin URLs)
from django.urls import path
from . import admin_views

urlpatterns = [
    path('login/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='admin_logout'),
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('bookings/', admin_views.booking_list, name='admin_booking_list'),
    path('booking/<int:booking_id>/', admin_views.booking_detail, name='booking_detail'),
    path('stats/', admin_views.get_booking_stats, name='admin_stats'),
]