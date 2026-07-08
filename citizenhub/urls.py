from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from accounts.get_token import get_token
from rest_framework_simplejwt.views import TokenRefreshView

def home(request):
    return JsonResponse({'message': 'Citizen Hub API', 'status': 'running'})

urlpatterns = [
    path('', home, name='home'),
    path('health/', include('citizenhub.health_urls')),
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/get-token/', get_token, name='get_token'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('accounts.urls')),
    
    # Apps
    path('api/constitution/', include('constitution.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]

# Add Swagger URLs
from .swagger_urls import urlpatterns as swagger_urlpatterns
urlpatterns += swagger_urlpatterns

# Static files
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
