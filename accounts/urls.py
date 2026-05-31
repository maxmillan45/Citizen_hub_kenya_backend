from django.urls import path
from .mpesa_views import (
    RequestSTKPushView,
    MPesaCallbackView,
    CheckAuthStatusView,
    QueryStatusView,
    TestAuthSuccessView
)
from .views import RegisterView, LoginView, LogoutView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('request/', RequestSTKPushView.as_view(), name='auth-request'),
    path('callback/', MPesaCallbackView.as_view(), name='auth-callback'),
    path('status/', CheckAuthStatusView.as_view(), name='auth-status'),
    path('query/', QueryStatusView.as_view(), name='query-status'),
    path('test-success/', TestAuthSuccessView.as_view(), name='test-success'),
]
