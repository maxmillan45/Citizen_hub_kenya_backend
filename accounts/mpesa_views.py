from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.conf import settings
import requests
import base64
from datetime import datetime
import json

class MPesaAuth:
    @staticmethod
    def get_access_token():
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        
        if not consumer_key or not consumer_secret:
            print("M-Pesa credentials missing")
            return None
        
        auth_string = f"{consumer_key}:{consumer_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {'Authorization': f'Basic {auth_base64}'}
        url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        
        try:
            print("Requesting M-Pesa access token...")
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Token response status: {response.status_code}")
            if response.status_code == 200:
                token = response.json().get('access_token')
                print(f"Token received: {token[:20]}...")
                return token
            else:
                print(f"Token error: {response.text}")
                return None
        except Exception as e:
            print(f"Token request error: {e}")
            return None

class RequestSTKPushView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            phone_number = request.data.get('phone_number')
            amount = request.data.get('amount', '1')
            account_reference = request.data.get('account_reference', 'CitizenHub')
            transaction_desc = request.data.get('transaction_desc', 'Payment')
            
            print(f"STK Push request - Phone: {phone_number}, Amount: {amount}")
            
            if not phone_number:
                return Response({'error': 'Phone number required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Format phone number
            if phone_number.startswith('0'):
                phone_number = '254' + phone_number[1:]
            elif phone_number.startswith('+'):
                phone_number = phone_number[1:]
            
            print(f"Formatted phone: {phone_number}")
            
            access_token = MPesaAuth.get_access_token()
            if not access_token:
                return Response({
                    'error': 'Failed to authenticate with M-Pesa. Check your credentials.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            passkey = settings.MPESA_PASSKEY
            shortcode = settings.MPESA_SHORTCODE
            
            if not passkey or not shortcode:
                return Response({
                    'error': 'M-Pesa shortcode or passkey not configured'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
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
                'CallBackURL': settings.MPESA_CALLBACK_URL or 'https://citizen-hub-kenya-backend.onrender.com/api/auth/stk/callback/',
                'AccountReference': account_reference,
                'TransactionDesc': transaction_desc
            }
            
            print(f"STK Push payload: {json.dumps(payload, indent=2)}")
            
            url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response_data = response.json()
            
            print(f"STK Push response: {json.dumps(response_data, indent=2)}")
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return Response({
                'error': f'Network error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MPesaCallbackView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            callback_data = request.data
            print("Callback received:", json.dumps(callback_data, indent=2))
            return Response({'ResultCode': 0, 'ResultDesc': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Callback error: {e}")
            return Response({'ResultCode': 1, 'ResultDesc': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QueryStatusView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, checkout_request_id):
        try:
            print(f"Querying status for: {checkout_request_id}")
            
            access_token = MPesaAuth.get_access_token()
            if not access_token:
                return Response({
                    'error': 'Failed to authenticate with M-Pesa'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
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
            response_data = response.json()
            
            print(f"Status response: {json.dumps(response_data, indent=2)}")
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TestAuthSuccessView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        return Response({'message': 'Test auth success', 'status': 'ok'})
