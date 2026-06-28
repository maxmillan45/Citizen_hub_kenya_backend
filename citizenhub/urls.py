from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from accounts.get_token import get_token
from rest_framework_simplejwt.views import TokenRefreshView
import citizenhub.health_views as health_views

def home(request):
    return JsonResponse({'message': 'Citizen Hub API', 'status': 'running'})

urlpatterns = [
    path('', home, name='home'),
    path('health/', health_views.HealthCheckView.as_view(), name='health'),
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/get-token/', get_token, name='get_token'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('accounts.urls')),
    
    # Apps
    path('api/constitution/', include('constitution.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from accounts.make_superuser_endpoint import make_superuser

urlpatterns += [
    path('api/make-superuser/', make_superuser, name='make_superuser'),
]
