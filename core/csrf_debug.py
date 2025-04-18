from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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