from django.urls import path
from .mpesa_views import RequestSTKPushView, QueryStatusView, TestAuthSuccessView
from .views import RegisterView, LoginView, LogoutView, ProfileView
from .feature_views import (
    DidYouKnowListView, DidYouKnowRandomView,
    FAQListView, MPListView,
    CrimeReportView, VotingStatusView, EventListView
)
from .user_stats import UserStatisticsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('stk/request/', RequestSTKPushView.as_view(), name='stk-request'),
    path('stk/query/', QueryStatusView.as_view(), name='stk-query'),
    path('test-success/', TestAuthSuccessView.as_view(), name='test-success'),
    path('history/', DidYouKnowListView.as_view(), name='history'),
    path('history/random/', DidYouKnowRandomView.as_view(), name='history-random'),
    path('faq/', FAQListView.as_view(), name='faq'),
    path('mp/', MPListView.as_view(), name='mp'),
    path('crime/', CrimeReportView.as_view(), name='crime'),
    path('voting/', VotingStatusView.as_view(), name='voting'),
    path('events/', EventListView.as_view(), name='events'),
    path('stats/', UserStatisticsView.as_view(), name='user-stats'),
]
from .mp_views import MPSearchView, MPCompareView, MPPerformanceDetailView

    path('mp/search/', MPSearchView.as_view(), name='mp-search'),
    path('mp/compare/', MPCompareView.as_view(), name='mp-compare'),
    path('mp/<int:mp_id>/performance/', MPPerformanceDetailView.as_view(), name='mp-performance'),
from .event_views import UpcomingEventsView, EventCountiesView, SetEventReminderView

    path('events/upcoming/', UpcomingEventsView.as_view(), name='events-upcoming'),
    path('events/counties/', EventCountiesView.as_view(), name='events-counties'),
    path('events/<int:event_id>/reminder/', SetEventReminderView.as_view(), name='event-reminder'),
