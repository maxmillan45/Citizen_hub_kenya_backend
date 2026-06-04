from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.urls import get_resolver

class URLListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        resolver = get_resolver()
        urls = []
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                for sub_pattern in pattern.url_patterns:
                    urls.append(str(sub_pattern.pattern))
            else:
                urls.append(str(pattern.pattern))
        return Response({
            'urls': urls[:50],
            'constitution_in_urls': any('constitution' in str(p) for p in urls)
        })
