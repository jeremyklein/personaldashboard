"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from core import views_debug
from core import csrf_debug
from core import csrf_test
import login_tests
import emergency

urlpatterns = [
    # Super emergency debug views with absolute minimal dependencies
    path('emergency/', emergency.debug_view),
    path('emergency/csrf/', emergency.set_csrf_cookie),
    path('emergency/post/', emergency.test_post),
    
    # Direct import emergency debug views
    path('exempt-direct/', login_tests.csrf_exempt_view),
    path('set-csrf-direct/', login_tests.set_csrf),
    path('debug-direct/', login_tests.debug_middleware),
    
    # Simplified CSRF exempt debug view
    path('exempt/', csrf_debug.test_exempt, name='csrf_exempt_test'),
    
    # CSRF cookie setter
    path('set-csrf-cookie/', csrf_test.set_csrf_cookie, name='set_csrf_cookie'),
    
    # Debug URLs for troubleshooting
    path('debug/info/', views_debug.debug_info, name='debug_info'),
    path('debug/csrf-form/', views_debug.test_csrf_form, name='test_csrf_form'),
    
    # Original URLs
    path('', include('core.urls')),
    path('tasks/', include('tasks.urls')),
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
]
