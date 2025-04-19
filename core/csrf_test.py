from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Remove login_required decorator from this view entirely
@ensure_csrf_cookie
@csrf_exempt  # Temporarily exempt for testing
def set_csrf_cookie(request):
    """View that explicitly sets a CSRF cookie"""
    # Bypass login required checks directly in the view
    print("===== SET CSRF COOKIE VIEW ACCESSED =====", flush=True)
    
    response = HttpResponse("CSRF Cookie has been set - testing direct access")
    
    # Print CSRF info for debugging
    print("CSRF cookie domain:", request.get_host(), flush=True)
    print("Is secure:", request.is_secure(), flush=True)
    
    return response