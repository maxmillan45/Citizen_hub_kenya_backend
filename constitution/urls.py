from django.urls import path
from .views import ArticleSearchView, ArticleDetailView

urlpatterns = [
    path('search/', ArticleSearchView.as_view(), name='article-search'),
    path('article/<str:article_number>/', ArticleDetailView.as_view(), name='article-detail'),
]

