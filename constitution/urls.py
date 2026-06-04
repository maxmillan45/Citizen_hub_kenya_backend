from django.urls import path
from .views import ArticleSearchView, ArticleDetailView

urlpatterns = [
    path('search/', ArticleSearchView.as_view(), name='article-search'),
    path('article/<str:article_number>/', ArticleDetailView.as_view(), name='article-detail'),
]

from .debug_view import DebugView

urlpatterns += [
    path('debug/', DebugView.as_view(), name='debug'),
]
from .test_only import TestOnlyView

urlpatterns += [
    path('test-only/', TestOnlyView.as_view(), name='test-only'),
]
