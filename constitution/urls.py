from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.ArticleSearchView.as_view(), name='article-search'),
    path('article/<str:article_number>/', views.ArticleDetailView.as_view(), name='article-detail'),
]
from .views import PopularArticlesView, ArticleCategoriesView, BookmarkArticleView, BookmarksListView

urlpatterns += [
    path('popular/', PopularArticlesView.as_view(), name='popular'),
    path('categories/', ArticleCategoriesView.as_view(), name='categories'),
    path('bookmark/<int:article_id>/', BookmarkArticleView.as_view(), name='bookmark'),
    path('bookmarks/', BookmarksListView.as_view(), name='bookmarks'),
]
