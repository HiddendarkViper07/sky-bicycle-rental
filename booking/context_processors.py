# booking/context_processors.py
from .models import SiteSettings

def site_settings(request):
    """Make site settings available in all templates"""
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    return {
        'site_settings': settings,
        'current_path': request.path,
    }