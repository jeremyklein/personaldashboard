"""
EMERGENCY DEBUG MODULE
Bypass all Django auth and middleware for testing
"""
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os

# Direct access to raw views without any middleware
@csrf_exempt
def debug_view(request):
    """Show debugging information without any middleware"""
    response_data = {
        'debug_mode': True,
        'method': request.method,
        'path': request.path,
        'GET': dict(request.GET),
        'POST': dict(request.POST),
        'cookies': dict(request.COOKIES),
        'headers': dict(request.headers),
        'META': {k: str(v) for k, v in request.META.items() if k.startswith('HTTP')},
        'user': str(request.user),
        'is_secure': request.is_secure(),
        'python_version': sys.version,
        'django_settings': {
            'DEBUG': os.environ.get('DEBUG', 'Not set'),
            'ALLOWED_HOSTS': os.environ.get('ALLOWED_HOSTS', 'Not set'),
            'SECRET_KEY_SET': bool(os.environ.get('SECRET_KEY')),
        }
    }
    
    # Print to console for Docker logs
    print("===== EMERGENCY DEBUG VIEW =====", flush=True)
    print(f"Method: {request.method}", flush=True)
    print(f"Path: {request.path}", flush=True)
    print(f"CSRF Cookie: {request.COOKIES.get('csrftoken', 'Not found')}", flush=True)
    
    # Return as formatted HTML
    html_response = f"""
    <html>
    <head>
        <title>Emergency Debug</title>
        <style>
            body {{ font-family: monospace; padding: 20px; }}
            pre {{ background: #f5f5f5; padding: 10px; overflow: auto; }}
        </style>
    </head>
    <body>
        <h1>Emergency Debug Information</h1>
        <pre>{json.dumps(response_data, indent=2)}</pre>
        
        <h2>Cookie Tester</h2>
        <div id="cookie-info"></div>
        
        <script>
            document.getElementById('cookie-info').innerHTML = 
                '<p>All cookies: ' + document.cookie + '</p>' +
                '<p>CSRF token: ' + (document.cookie.match(/csrftoken=([^;]+)/) ? 
                    document.cookie.match(/csrftoken=([^;]+)/)[1] : 'Not found') + '</p>';
        </script>
    </body>
    </html>
    """
    
    response = HttpResponse(html_response)
    response['Content-Type'] = 'text/html'
    return response

@csrf_exempt
def set_csrf_cookie(request):
    """Set CSRF cookie directly"""
    from django.middleware.csrf import get_token
    
    # Force a CSRF cookie to be set
    csrf_token = get_token(request)
    
    response = HttpResponse(f"CSRF token set: {csrf_token}")
    response['X-CSRFToken'] = csrf_token
    return response

@csrf_exempt
def test_post(request):
    """Test POST requests with CSRF exemption"""
    if request.method == 'POST':
        return HttpResponse(f"POST successful! Data: {dict(request.POST)}")
    
    return HttpResponse("""
    <form method="post">
        <input type="text" name="test_field" value="test_value">
        <button type="submit">Submit POST</button>
    </form>
    """)