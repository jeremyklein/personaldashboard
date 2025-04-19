"""
This module provides CSRF debug views for Django
Place directly in your project root and import
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json

@csrf_exempt
def csrf_exempt_view(request):
    """Simple view that's exempted from CSRF protection"""
    return HttpResponse('CSRF Exempt view working!')

@ensure_csrf_cookie
def set_csrf(request):
    """Explicitly set the CSRF cookie"""
    data = {
        'csrfCookieSet': True,
        'method': request.method,
        'host': request.get_host(),
        'isSecure': request.is_secure(),
        'cookies': {k: v for k, v in request.COOKIES.items()},
    }
    
    return HttpResponse(
        f'<pre>{json.dumps(data, indent=4)}</pre>',
        content_type='text/html'
    )

def debug_middleware(request):
    """View to bypass all middleware"""
    return HttpResponse("""
    <html>
    <body>
        <h1>Debug Page - No Middleware</h1>
        <script>
            document.write('<p>CSRF Cookie: ' + (document.cookie.match(/csrftoken=([^;]+)/) ? document.cookie.match(/csrftoken=([^;]+)/)[1] : 'Not set') + '</p>');
            document.write('<p>All Cookies: ' + document.cookie + '</p>');
        </script>
    </body>
    </html>
    """)