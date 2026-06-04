from django.http import JsonResponse
from .models import Article

def test_articles(request):
    articles = Article.objects.all().values('article_number', 'title', 'full_text')
    return JsonResponse(list(articles), safe=False)
