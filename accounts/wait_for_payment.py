from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
import requests
import base64
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

class WaitForPaymentView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        checkout_request_id = request.data.get('checkout_request_id')
        phone_number = request.data.get('phone_number')
        
        if not checkout_request_id:
            return Response({'success': False, 'message': 'CheckoutRequestID required'}, status=400)
        
        if not phone_number:
            return Response({'success': False, 'message': 'Phone number required'}, status=400)
        
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number.startswith('+'):
            phone_number = phone_number[1:]
        
        # Poll for up to 60 seconds (12 attempts * 5 seconds)
        max_attempts = 12
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            logger.info(f"Checking payment status, attempt {attempt}/{max_attempts}")
            
            try:
                # Get M-Pesa access token
                consumer_key = settings.MPESA_CONSUMER_KEY
                consumer_secret = settings.MPESA_CONSUMER_SECRET
                
                auth_string = f"{consumer_key}:{consumer_secret}"
                auth_bytes = auth_string.encode('ascii')
                auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
                
                auth_headers = {'Authorization': f'Basic {auth_base64}'}
                auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
                
                auth_response = requests.get(auth_url, headers=auth_headers, timeout=30)
                access_token = auth_response.json().get('access_token')
                
                if not access_token:
                    return Response({'success': False, 'message': 'Failed to authenticate with M-Pesa'}, status=500)
                
                # Query transaction status
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
                query_response = requests.post(query_url, json=payload, headers=query_headers, timeout=30)
                result = query_response.json()
                
                logger.info(f"Status check result: {result}")
                
                # Check if payment is complete
                if result.get('ResultCode') == '0':
                    # Payment successful
                    from django.contrib.auth import get_user_model
                    from rest_framework_simplejwt.tokens import RefreshToken
                    User = get_user_model()
                    
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
                elif result.get('ResultCode') == '1037':
                    return Response({
                        'success': False,
                        'message': 'Transaction cancelled by user'
                    }, status=400)
                elif result.get('ResultCode') == '1032':
                    return Response({
                        'success': False,
                        'message': 'Transaction failed. Please try again.'
                    }, status=400)
                elif result.get('fault'):
                    # Rate limit or other error - continue polling
                    logger.warning(f"M-Pesa fault: {result.get('fault')}")
                    if 'Spike arrest' in str(result.get('fault')):
                        time.sleep(5)  # Wait longer on rate limit
                        continue
                
            except Exception as e:
                logger.error(f"Payment check error: {e}")
            
            # Wait 5 seconds before next attempt
            time.sleep(5)
        
        # Timeout
        return Response({
            'success': False,
            'message': 'Payment timed out. Please try again.'
        }, status=408)
