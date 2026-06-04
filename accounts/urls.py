from django.urls import path
from .mpesa_views import RequestSTKPushView, TestAuthSuccessView
from .views import RegisterView, LoginView, LogoutView, ProfileView
from .feature_views import (
    DidYouKnowListView, DidYouKnowRandomView,
    FAQListView, MPListView,
    CrimeReportView, VotingStatusView, EventListView
)
from .migration_views import RunMigrationsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('stk/request/', RequestSTKPushView.as_view(), name='stk-request'),
    path('test-success/', TestAuthSuccessView.as_view(), name='test-success'),
    path('history/', DidYouKnowListView.as_view(), name='history'),
    path('history/random/', DidYouKnowRandomView.as_view(), name='history-random'),
    path('faq/', FAQListView.as_view(), name='faq'),
    path('mp/', MPListView.as_view(), name='mp'),
    path('crime/', CrimeReportView.as_view(), name='crime'),
    path('voting/', VotingStatusView.as_view(), name='voting'),
    path('events/', EventListView.as_view(), name='events'),
    path('migrate/', RunMigrationsView.as_view(), name='migrate'),
]
from .constitution_proxy import ConstitutionSearchProxy

    path('constitution-search/', ConstitutionSearchProxy.as_view(), name='constitution-search'),
