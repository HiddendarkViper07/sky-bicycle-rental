# sky_rental/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from booking import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin (optional)
    path('', include('booking.urls')),  # User URLs
    path('admin-panel/', include('booking.admin_urls')),  # Custom admin
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)