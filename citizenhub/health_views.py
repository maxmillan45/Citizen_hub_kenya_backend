from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import connections
from django.db.utils import OperationalError
from django.core.cache import cache
import requests
import os

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        health_status = {
            'status': 'healthy',
            'timestamp': None,
            'database': 'unknown',
            'cache': 'unknown',
            'mpesa': 'unknown',
            'chatbot': 'unknown'
        }
        
        from django.utils import timezone
        health_status['timestamp'] = timezone.now().isoformat()
        
        # Check database
        try:
            db_conn = connections['default']
            db_conn.cursor()
            health_status['database'] = 'connected'
        except OperationalError:
            health_status['database'] = 'disconnected'
            health_status['status'] = 'unhealthy'
        
        # Check cache (Redis)
        try:
            cache.set('health_check', 'ok', 10)
            if cache.get('health_check') == 'ok':
                health_status['cache'] = 'connected'
            else:
                health_status['cache'] = 'error'
        except Exception:
            health_status['cache'] = 'disconnected'
        
        # Check M-Pesa API (optional)
        if os.getenv('ENABLE_MPESA') == 'True':
            try:
                # Just check if endpoint is reachable
                response = requests.get('https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', 
                                      timeout=5)
                health_status['mpesa'] = 'reachable' if response.status_code < 500 else 'error'
            except requests.RequestException:
                health_status['mpesa'] = 'unreachable'
        
        # Check chatbot (OpenAI API)
        if os.getenv('ENABLE_CHATBOT') == 'True':
            try:
                # Lightweight check without making actual API call
                health_status['chatbot'] = 'configured'
            except Exception:
                health_status['chatbot'] = 'error'
        
        return Response(health_status)
