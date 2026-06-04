from django.urls import path
from .test_only import TestOnlyView
from .views import ArticleSearchView, ArticleDetailView

urlpatterns = [
    path('test-only/', TestOnlyView.as_view(), name='test-only'),
    path('search/', ArticleSearchView.as_view(), name='article-search'),
    path('article/<str:article_number>/', ArticleDetailView.as_view(), name='article-detail'),
]
from .health_check import URLListView

urlpatterns += [
    path('urls/', URLListView.as_view(), name='url-list'),
]
