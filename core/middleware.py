from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            # Paths that don't require authentication
            allowed_paths = [
                reverse('login'),
                reverse('register'),
                reverse('logout'),
                '/admin/',
                '/admin/login/',
                '/__reload__/',
                '/static/'
            ]
            
            # Check if current path is in the allowed paths
            if not any(request.path.startswith(path) for path in allowed_paths):
                return redirect('login')
                
        response = self.get_response(request)
        return response