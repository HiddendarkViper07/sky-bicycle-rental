# booking/decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_login_required(view_func):
    """Decorator to check if admin is logged in"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            messages.error(request, 'Please login to access admin panel')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

def prevent_cache(view_func):
    """Prevent browser caching for sensitive pages"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper