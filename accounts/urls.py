from django.urls import path
from .mpesa_views import RequestSTKPushView, TestAuthSuccessView
from .views import RegisterView, LoginView, LogoutView, ProfileView
from .feature_views import (
    DidYouKnowListView, DidYouKnowRandomView,
    FAQListView, MPListView,
    CrimeReportView, VotingStatusView, EventListView
)
from .load_data_view import LoadDataView

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # M-Pesa STK
    path('stk/request/', RequestSTKPushView.as_view(), name='stk-request'),
    path('test-success/', TestAuthSuccessView.as_view(), name='test-success'),
    
    # Did You Know - History
    path('history/', DidYouKnowListView.as_view(), name='history'),
    path('history/random/', DidYouKnowRandomView.as_view(), name='history-random'),
    
    # FAQ
    path('faq/', FAQListView.as_view(), name='faq'),
    
    # MP Scorecard
    path('mp/', MPListView.as_view(), name='mp'),
    
    # Crime Reporting
    path('crime/', CrimeReportView.as_view(), name='crime'),
    
    # Voting
    path('voting/', VotingStatusView.as_view(), name='voting'),
    
    # Public Events
    path('events/', EventListView.as_view(), name='events'),
    
    # Data Status
    path('data-status/', LoadDataView.as_view(), name='data-status'),
]
