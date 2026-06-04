from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.ArticleSearchView.as_view(), name='article-search'),
    path('article/<str:article_number>/', views.ArticleDetailView.as_view(), name='article-detail'),
]
