from django.urls import path
from . import views
from . import feature_views
from . import mpesa_views
from . import crud_views
from . import admin_analytics
from .admin_monitoring import (
    DashboardStatsView, UserManagementView, CrimeReportManagementView,
    FAQManagementView, PaymentMonitoringView, SystemSettingsView
)
from rest_framework_simplejwt.views import TokenRefreshView
from .simple_auth_view import SimpleMPesaAuthenticateView
from .test_token_view import TestTokenView

urlpatterns = [
    # M-Pesa Authentication
    path('stk/request/', mpesa_views.RequestSTKPushView.as_view(), name='stk-request'),
    path('stk/status/<str:checkout_request_id>/', mpesa_views.QueryStatusView.as_view(), name='stk-status'),
    path('stk/callback/', mpesa_views.MPesaCallbackView.as_view(), name='stk-callback'),
    path('mpesa/authenticate/', SimpleMPesaAuthenticateView.as_view(), name='mpesa-authenticate'),
    path('test-token/', TestTokenView.as_view(), name='test-token'),
    
    # User Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('complete-profile/', views.CompleteProfileView.as_view(), name='complete-profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Feature endpoints
    path('history/', feature_views.DidYouKnowListView.as_view(), name='history'),
    path('faq/', feature_views.FAQListView.as_view(), name='faq-list'),
    path('faq/<int:pk>/', crud_views.FAQDetailView.as_view(), name='faq-detail'),
    path('mp/', feature_views.MPListView.as_view(), name='mp-list'),
    path('mp/<int:pk>/', crud_views.MPDetailView.as_view(), name='mp-detail'),
    path('events/', feature_views.EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', crud_views.EventDetailView.as_view(), name='event-detail'),
    path('crime/', feature_views.CrimeReportView.as_view(), name='crime-report'),
    path('voting/', feature_views.VotingStatusView.as_view(), name='voting-status'),
    
    # Bulk operations
    path('faq/bulk-delete/', crud_views.BulkFAQDeleteView.as_view(), name='faq-bulk-delete'),
    path('crime/export/csv/', crud_views.ExportCrimeReportsView.as_view(), name='crime-export'),
    
    # Admin endpoints
    path('admin/stats/', admin_analytics.AdminStatsView.as_view(), name='admin-stats'),
    path('admin/dashboard/', DashboardStatsView.as_view(), name='admin-dashboard'),
    path('admin/users/', UserManagementView.as_view(), name='admin-users'),
    path('admin/users/<int:user_id>/', UserManagementView.as_view(), name='admin-user-update'),
    path('admin/crimes/', CrimeReportManagementView.as_view(), name='admin-crimes'),
    path('admin/crimes/<int:report_id>/', CrimeReportManagementView.as_view(), name='admin-crime-update'),
    path('admin/faqs/', FAQManagementView.as_view(), name='admin-faqs'),
    path('admin/payments/', PaymentMonitoringView.as_view(), name='admin-payments'),
    path('admin/settings/', SystemSettingsView.as_view(), name='admin-settings'),
]
from .direct_token import get_token_direct

urlpatterns += [
    path('get-token/', get_token_direct, name='get-token-direct'),
]
