from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

@csrf_exempt
def test_exempt(request):
    """Debug view with CSRF exemption"""
    response_content = f"""
    Request method: {request.method}
    Request path: {request.path}
    Host: {request.get_host()}
    Is secure: {request.is_secure()}
    """
    
    # Print to server logs
    print("=== CSRF DEBUG VIEW ACCESSED ===", flush=True)
    print(response_content, flush=True)
    
    # Create and return response
    response = HttpResponse(f"<pre>{response_content}</pre>")
    response["X-CSRF-DEBUG"] = "CSRF check bypassed with csrf_exempt"
    
    return response

def debug_headers(request):
    """Debug view that returns all request headers as JSON."""
    headers = {key.replace('HTTP_', ''): value for key, value in request.META.items() 
              if key.startswith('HTTP_') or key in ('CONTENT_TYPE', 'CONTENT_LENGTH')}
    
    # Add CSRF specific info
    csrf_cookie = request.COOKIES.get('csrftoken', 'Not present')
    csrf_header = request.META.get('HTTP_X_CSRFTOKEN', 'Not present')
    
    debug_info = {
        'headers': headers,
        'csrf_cookie': csrf_cookie,
        'csrf_header': csrf_header,
        'cookies': request.COOKIES,
    }
    
    print("=== DEBUG HEADERS REQUEST ===", flush=True)
    print(f"CSRF Cookie: {csrf_cookie}", flush=True)
    print(f"CSRF Header: {csrf_header}", flush=True)
    
    return JsonResponse(debug_info)