from django.urls import path
from . import views
from . import feature_views
from . import mpesa_views
from . import crud_views
from . import admin_analytics

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('test-success/', views.TestAuthSuccessView.as_view(), name='test-success'),
    path('stk/request/', mpesa_views.RequestSTKPushView.as_view(), name='stk-request'),
    path('stk/callback/', mpesa_views.MPesaCallbackView.as_view(), name='stk-callback'),
    path('history/', feature_views.DidYouKnowListView.as_view(), name='history'),
    path('faq/', feature_views.FAQListView.as_view(), name='faq-list'),
    path('mp/', feature_views.MPListView.as_view(), name='mp-list'),
    path('events/', feature_views.EventListView.as_view(), name='event-list'),
    path('crime/', feature_views.CrimeReportView.as_view(), name='crime-report'),
    path('voting/', feature_views.VotingStatusView.as_view(), name='voting-status'),
    path('faq/<uuid:pk>/', crud_views.FAQDetailView.as_view(), name='faq-detail'),
    path('mp/<uuid:pk>/', crud_views.MPDetailView.as_view(), name='mp-detail'),
    path('faq/bulk-delete/', crud_views.BulkFAQDeleteView.as_view(), name='faq-bulk-delete'),
    path('crime/export/csv/', crud_views.ExportCrimeReportsView.as_view(), name='crime-export'),
    path('admin/stats/', admin_analytics.AdminStatsView.as_view(), name='admin-stats'),
]
from .admin_monitoring import (
    DashboardStatsView, UserManagementView, CrimeReportManagementView,
    FAQManagementView, PaymentMonitoringView, SystemSettingsView
)

urlpatterns += [
    path('admin/dashboard/', DashboardStatsView.as_view(), name='admin-dashboard'),
    path('admin/users/', UserManagementView.as_view(), name='admin-users'),
    path('admin/users/<uuid:user_id>/', UserManagementView.as_view(), name='admin-user-update'),
    path('admin/crimes/', CrimeReportManagementView.as_view(), name='admin-crimes'),
    path('admin/crimes/<uuid:report_id>/', CrimeReportManagementView.as_view(), name='admin-crime-update'),
    path('admin/faqs/', FAQManagementView.as_view(), name='admin-faqs'),
    path('admin/payments/', PaymentMonitoringView.as_view(), name='admin-payments'),
    path('admin/settings/', SystemSettingsView.as_view(), name='admin-settings'),
]
from .views import LogoutView, ChangePasswordView, ForgotPasswordView

urlpatterns += [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
]
