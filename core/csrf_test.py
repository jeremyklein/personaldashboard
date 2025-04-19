from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def set_csrf_cookie(request):
    """View that explicitly sets a CSRF cookie"""
    response = HttpResponse("CSRF Cookie has been set")
    
    # Print CSRF info for debugging
    print("CSRF cookie domain:", request.get_host(), flush=True)
    print("Is secure:", request.is_secure(), flush=True)
    
    return response