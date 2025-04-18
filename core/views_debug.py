from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys

@csrf_exempt
def debug_info(request):
    """Debug view to show request information"""
    debug_data = {
        "method": request.method,
        "path": request.path,
        "host": request.get_host(),
        "secure": request.is_secure(),
        "headers": dict(request.headers),
        "META": {k: str(v) for k, v in request.META.items() if k.startswith('HTTP_') or k in ('REMOTE_ADDR', 'SERVER_NAME')},
        "cookies": request.COOKIES,
        "python_version": sys.version,
    }
    
    # Directly print to stdout for Docker logs
    print("DEBUG VIEW ACCESSED", flush=True)
    print(f"DEBUG DATA: {json.dumps(debug_data, indent=2)}", flush=True)
    
    response = HttpResponse(
        f"<pre>DEBUG INFO:\n{json.dumps(debug_data, indent=4)}</pre>",
        content_type="text/html"
    )
    
    return response

@csrf_exempt
def test_csrf_form(request):
    """Test CSRF form submission"""
    if request.method == 'POST':
        print("POST DATA:", dict(request.POST), flush=True)
        return HttpResponse("POST received successfully!")
    
    return HttpResponse("""
    <html>
    <head><title>CSRF Test Form</title></head>
    <body>
        <h1>Manual CSRF Test Form</h1>
        
        <form method="post">
            <input type="text" name="username" value="testuser">
            <input type="submit" value="Submit">
        </form>
        
        <h1>Form with CSRF Token</h1>
        <form method="post" action="/register/">
            <input type="hidden" name="csrfmiddlewaretoken" id="csrftoken" value="">
            <input type="text" name="username" value="testuser">
            <input type="submit" value="Submit">
        </form>
        
        <script>
            // Function to get CSRF token from cookie
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            
            // Set CSRF token in form
            window.onload = function() {
                const csrftoken = getCookie('csrftoken');
                document.getElementById('csrftoken').value = csrftoken || '';
                console.log("CSRF Token:", csrftoken);
            };
        </script>
    </body>
    </html>
    """)