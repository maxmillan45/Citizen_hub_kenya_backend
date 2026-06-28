from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
import requests
import base64
import time
from datetime import datetime

User = get_user_model()

class MPesaWaitPaymentView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        checkout_request_id = request.data.get('checkout_request_id')
        phone_number = request.data.get('phone_number')
        
        if not checkout_request_id:
            return Response({'error': 'CheckoutRequestID required'}, status=400)
        
        if phone_number and phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number and phone_number.startswith('+'):
            phone_number = phone_number[1:]
        
        # Poll for 60 seconds (8 attempts * 8 seconds = 64 seconds)
        max_attempts = 8
        wait_time = 8
        
        for attempt in range(max_attempts):
            time.sleep(wait_time)
            
            try:
                consumer_key = settings.MPESA_CONSUMER_KEY
                consumer_secret = settings.MPESA_CONSUMER_SECRET
                
                auth_string = f"{consumer_key}:{consumer_secret}"
                auth_bytes = auth_string.encode('ascii')
                auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
                
                headers = {'Authorization': f'Basic {auth_base64}'}
                auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
                
                auth_response = requests.get(auth_url, headers=headers, timeout=10)
                access_token = auth_response.json().get('access_token')
                
                if not access_token:
                    continue
                
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                shortcode = settings.MPESA_SHORTCODE
                passkey = settings.MPESA_PASSKEY
                
                password_str = f"{shortcode}{passkey}{timestamp}"
                password_bytes = password_str.encode('ascii')
                password = base64.b64encode(password_bytes).decode('ascii')
                
                query_headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'BusinessShortCode': shortcode,
                    'Password': password,
                    'Timestamp': timestamp,
                    'CheckoutRequestID': checkout_request_id
                }
                
                query_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
                query_response = requests.post(query_url, json=payload, headers=query_headers, timeout=10)
                result = query_response.json()
                
                print(f"Wait attempt {attempt + 1}: {result}")
                
                if result.get('ResultCode') == '0':
                    user, created = User.objects.get_or_create(
                        phone_number=phone_number
                    )
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'success': True,
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'user_id': user.id,
                        'phone_number': phone_number,
                        'is_new_user': created
                    })
                elif result.get('ResultCode') in ['1037', '1032']:
                    return Response({
                        'success': False,
                        'message': result.get('ResultDesc', 'Transaction failed')
                    }, status=400)
                elif result.get('fault'):
                    print(f"Fault: {result.get('fault')}")
                    continue
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} error: {e}")
                continue
        
        return Response({
            'success': False,
            'message': 'Payment timed out. Please try again.'
        }, status=408)
