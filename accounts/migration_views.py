from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.management import call_command
from io import StringIO

class RunMigrationsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        key = request.query_params.get('key')
        if key != 'migrate_citizen_hub_2026':
            return Response({'error': 'Invalid key'}, status=403)
        
        out = StringIO()
        try:
            call_command('migrate', stdout=out)
            return Response({'status': 'success', 'output': out.getvalue()})
        except Exception as e:
            return Response({'status': 'error', 'error': str(e)}, status=500)
