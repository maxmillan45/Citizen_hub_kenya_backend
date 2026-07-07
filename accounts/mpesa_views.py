from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.conf import settings
import requests
import base64
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class MPesaAuth:
    @staticmethod
    def get_access_token():
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        
        if not consumer_key or not consumer_secret:
            logger.error("M-Pesa credentials not configured")
            return None
        
        auth_string = f"{consumer_key}:{consumer_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {'Authorization': f'Basic {auth_base64}'}
        url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            token = response.json().get('access_token')
            logger.info("M-Pesa access token obtained successfully")
            return token
        except Exception as e:
            logger.error(f"M-Pesa auth error: {e}")
            return None

class RequestSTKPushView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            phone_number = request.data.get('phone_number')
            amount = request.data.get('amount', '1')
            account_reference = request.data.get('account_reference', 'CitizenHub')
            transaction_desc = request.data.get('transaction_desc', 'Payment')
            
            if not phone_number:
                return Response({'error': 'Phone number required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            elif phone_number.startswith('+'):
                phone_number = phone_number[1:]
            
            access_token = MPesaAuth.get_access_token()
            if not access_token:
                return Response({'error': 'Failed to authenticate with M-Pesa. Check your credentials.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            passkey = settings.MPESA_PASSKEY
            shortcode = settings.MPESA_SHORTCODE
            
            password_str = f"{shortcode}{passkey}{timestamp}"
            password_bytes = password_str.encode('ascii')
            password = base64.b64encode(password_bytes).decode('ascii')
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': shortcode,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': amount,
                'PartyA': phone_number,
                'PartyB': shortcode,
                'PhoneNumber': phone_number,
                'CallBackURL': settings.MPESA_CALLBACK_URL,
                'AccountReference': account_reference,
                'TransactionDesc': transaction_desc
            }
            
            url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response_data = response.json()
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MPesaCallbackView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            callback_data = request.data
            print("Callback received:", json.dumps(callback_data, indent=2))
            return Response({'ResultCode': 0, 'ResultDesc': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'ResultCode': 1, 'ResultDesc': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QueryStatusView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, checkout_request_id):
        try:
            access_token = MPesaAuth.get_access_token()
            if not access_token:
                return Response({'error': 'Failed to authenticate'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            shortcode = settings.MPESA_SHORTCODE
            passkey = settings.MPESA_PASSKEY
            
            password_str = f"{shortcode}{passkey}{timestamp}"
            password_bytes = password_str.encode('ascii')
            password = base64.b64encode(password_bytes).decode('ascii')
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': shortcode,
                'Password': password,
                'Timestamp': timestamp,
                'CheckoutRequestID': checkout_request_id
            }
            
            url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            return Response(response.json(), status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MPesaAuthenticateView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        checkout_request_id = request.data.get('checkout_request_id')
        phone_number = request.data.get('phone_number')
        
        if not checkout_request_id:
            return Response({'error': 'CheckoutRequestID required'}, status=400)
        
        if not phone_number:
            return Response({'error': 'Phone number required'}, status=400)
        
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number.startswith('+'):
            phone_number = phone_number[1:]
        
        try:
            from django.contrib.auth import get_user_model
            from rest_framework_simplejwt.tokens import RefreshToken
            User = get_user_model()
            
            # First, check if we already have a successful transaction in the database
            # For now, let's query the status once and trust it
            access_token = MPesaAuth.get_access_token()
            if not access_token:
                return Response({'success': False, 'message': 'Failed to authenticate with M-Pesa'}, status=500)
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            shortcode = settings.MPESA_SHORTCODE
            passkey = settings.MPESA_PASSKEY
            
            password_str = f"{shortcode}{passkey}{timestamp}"
            password_bytes = password_str.encode('ascii')
            password = base64.b64encode(password_bytes).decode('ascii')
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': shortcode,
                'Password': password,
                'Timestamp': timestamp,
                'CheckoutRequestID': checkout_request_id
            }
            
            url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            result = response.json()
            
            print(f"Authenticate query result: {result}")
            
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
                    'phone_number': user.phone_number,
                    'is_new_user': created
                })
            else:
                return Response({
                    'success': False,
                    'message': result.get('ResultDesc', 'Payment not completed'),
                    'result_code': result.get('ResultCode')
                }, status=400)
                
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)

class TestAuthSuccessView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        return Response({'message': 'Test auth success', 'status': 'ok'})
