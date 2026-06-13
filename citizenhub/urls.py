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
