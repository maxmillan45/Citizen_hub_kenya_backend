from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Citizen Hub Kenya API",
        default_version='v1',
        description="""
        Citizen Hub Kenya API Documentation
        
        ## Authentication
        This API uses JWT authentication. To authenticate:
        1. Use the `/api/get-token/` endpoint to get an access token
        2. Include the token in the Authorization header: `Bearer <token>`
        
        ## M-Pesa Authentication Flow
        1. Request STK push: `/api/auth/stk/request/`
        2. User enters PIN on phone
        3. Check status: `/api/auth/stk/status/{checkout_id}/`
        4. Get token: `/api/auth/mpesa/authenticate/`
        
        ## Public Endpoints (No Authentication Required)
        - `/api/auth/history/` - Kenyan history facts
        - `/api/auth/faq/` - Legal FAQs
        - `/api/auth/mp/` - Members of Parliament
        - `/api/auth/events/` - Public events
        - `/api/constitution/search/` - Search constitution
        - `/api/constitution/article/{number}/` - Get specific article
        - `/health/` - Health check
        
        ## Protected Endpoints (Authentication Required)
        - `/api/auth/profile/` - User profile
        - `/api/auth/crime/` - Crime reporting
        - `/api/chatbot/ask/` - AI Legal Assistant
        - `/api/chatbot/history/` - Chat history
        - `/api/auth/complete-profile/` - Complete profile
        - `/api/auth/admin-panel/*` - Admin endpoints
        
        ## Admin Endpoints
        All admin endpoints require superuser privileges and use the same JWT token.
        """,
        terms_of_service="https://www.citizenhub.co.ke/terms/",
        contact=openapi.Contact(
            email="support@citizenhub.co.ke",
            name="Citizen Hub Support",
            url="https://www.citizenhub.co.ke"
        ),
        license=openapi.License(
            name="MIT License",
            url="https://opensource.org/licenses/MIT"
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
