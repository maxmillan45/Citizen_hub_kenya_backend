from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Citizen Hub Kenya API",
        default_version='v1',
        description="API for Citizen Hub Kenya - Constitutional Rights Platform",
        terms_of_service="https://www.citizenhub.ke/terms/",
        contact=openapi.Contact(email="info@citizenhub.ke"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('health_check.urls') if 'health_check' in settings.INSTALLED_APPS else lambda: [],),
    path('api/auth/', include('accounts.urls')),
    path('api/constitution/', include('constitution.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    
    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
