import requests
import base64
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from .models import User

class MPesaAuth:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.passkey = settings.MPESA_PASSKEY
        self.shortcode = settings.MPESA_SHORTCODE
        self.environment = getattr(settings, 'MPESA_ENVIRONMENT', 'sandbox')
        
        if self.environment == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
    
    def get_access_token(self):
        cache_key = 'mpesa_access_token'
        token = cache.get(cache_key)
        if token:
            return token
        
        auth_url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {'Authorization': f'Basic {auth_b64}'}
        response = requests.get(auth_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            cache.set(cache_key, token, timeout=3500)
            return token
        return None

mpesa_auth = MPesaAuth()

class RequestSTKPushView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number required'}, status=400)
        
        if phone_number.startswith('0'):
            formatted = '254' + phone_number[1:]
        else:
            formatted = phone_number
        
        token = mpesa_auth.get_access_token()
        if not token:
            return Response({'error': 'Failed to authenticate with M-Pesa'}, status=500)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f"{mpesa_auth.shortcode}{mpesa_auth.passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()
        
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        payload = {
            'BusinessShortCode': mpesa_auth.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': 1,
            'PartyA': formatted,
            'PartyB': mpesa_auth.shortcode,
            'PhoneNumber': formatted,
            'CallBackURL': settings.MPESA_CALLBACK_URL,
            'AccountReference': 'CITIZEN_HUB_AUTH',
            'TransactionDesc': 'Identity Verification'
        }
        
        response = requests.post(
            f"{mpesa_auth.base_url}/mpesa/stkpush/v1/processrequest",
            headers=headers, json=payload, timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return Response({
                'message': 'Check your M-Pesa app',
                'checkout_request_id': data.get('CheckoutRequestID'),
                'response_code': data.get('ResponseCode'),
                'response_description': data.get('ResponseDescription')
            })
        return Response({'error': 'STK push failed', 'details': response.text}, status=500)


class MPesaCallbackView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        print(f"Callback received: {request.data}")
        return Response({'ResultCode': 0, 'ResultDesc': 'Success'})


class CheckAuthStatusView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        return Response({'status': 'pending'})


class QueryStatusView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        checkout_request_id = request.data.get('checkout_request_id')
        if not checkout_request_id:
            return Response({'error': 'Checkout request ID required'}, status=400)
        
        token = mpesa_auth.get_access_token()
        if not token:
            return Response({'status': 'pending', 'message': 'Getting token...'})
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = f"{mpesa_auth.shortcode}{mpesa_auth.passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()
        
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        payload = {
            'BusinessShortCode': mpesa_auth.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id
        }
        
        try:
            response = requests.post(
                f"{mpesa_auth.base_url}/mpesa/stkpushquery/v1/query",
                headers=headers, json=payload, timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                result_code = data.get('ResultCode')
                if result_code == '0':
                    return Response({'status': 'success', 'message': 'Authenticated successfully'})
                elif result_code == '1037':
                    return Response({'status': 'pending', 'message': 'Waiting for PIN entry'})
                else:
                    return Response({'status': 'failed', 'message': data.get('ResultDesc')})
        except Exception:
            pass
        return Response({'status': 'pending', 'message': 'Processing...'})


class TestAuthSuccessView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number required'}, status=400)
        
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'is_active': True}
        )
        user.last_active = timezone.now()
        user.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'phone_number': user.phone_number,
                'civic_score': user.civic_score,
                'account_type': user.account_type
            }
        })
