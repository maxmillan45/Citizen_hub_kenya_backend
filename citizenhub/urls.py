from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'Citizen Hub API is running'})

urlpatterns = [
    path('health/', health_check, name='health'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/constitution/', include('constitution.urls')),
    path('api/chatbot/', include('chatbot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from .health_views import HealthCheckView

# Add to urlpatterns:
# path('health/', HealthCheckView.as_view(), name='health-check'),
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns += [
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
from accounts.simple_token import generate_token

urlpatterns += [
    path('api/token/', generate_token, name='generate_token'),
]
from accounts.token_view import get_access_token

urlpatterns += [
    path('api/get-token/', get_access_token, name='get_token'),
]
from accounts.token_view import get_access_token

urlpatterns += [
    path('api/get-token/', get_access_token, name='get_token'),
]
