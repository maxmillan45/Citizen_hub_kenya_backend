from django.urls import path
from . import views
from .test_view import test_articles

urlpatterns = [
    path('search/', views.ArticleSearchView.as_view(), name='article-search'),
    path('article/<str:article_number>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('test-articles/', test_articles, name='test-articles'),
]
