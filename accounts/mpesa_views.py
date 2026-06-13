from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.conf import settings
import requests
import json
import base64
from datetime import datetime
from .models import MpesaTransaction

class MPesaAuth:
    @staticmethod
    def get_access_token():
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        
        if not consumer_key or not consumer_secret:
            return None
        
        auth_string = f"{consumer_key}:{consumer_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_base64}'
        }
        
        url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.RequestException:
            return None

class RequestSTKPushView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')
        account_reference = request.data.get('account_reference', 'CitizenHub')
        transaction_desc = request.data.get('transaction_desc', 'Payment to Citizen Hub')
        
        if not phone_number or not amount:
            return Response({
                'error': 'Phone number and amount are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Format phone number (remove 0 or +254)
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number.startswith('+'):
            phone_number = phone_number[1:]
        
        access_token = MPesaAuth.get_access_token()
        if not access_token:
            return Response({
                'error': 'Failed to authenticate with M-Pesa'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response_data = response.json()
            
            # Save transaction
            MpesaTransaction.objects.create(
                phone_number=phone_number,
                amount=amount,
                account_reference=account_reference,
                transaction_desc=transaction_desc,
                checkout_request_id=response_data.get('CheckoutRequestID'),
                response_code=response_data.get('ResponseCode'),
                response_description=response_data.get('ResponseDescription')
            )
            
            return Response(response_data)
        except requests.RequestException as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MPesaCallbackView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        callback_data = request.data
        
        try:
            body = callback_data.get('Body', {})
            stk_callback = body.get('stkCallback', {})
            
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            
            # Update transaction
            transaction = MpesaTransaction.objects.filter(
                checkout_request_id=checkout_request_id
            ).first()
            
            if transaction:
                transaction.result_code = result_code
                transaction.result_description = result_desc
                transaction.is_completed = (result_code == '0')
                
                if result_code == '0':
                    callback_metadata = stk_callback.get('CallbackMetadata', {})
                    items = callback_metadata.get('Item', [])
                    for item in items:
                        if item.get('Name') == 'Amount':
                            transaction.amount = item.get('Value')
                        elif item.get('Name') == 'MpesaReceiptNumber':
                            transaction.mpesa_receipt_number = item.get('Value')
                        elif item.get('Name') == 'TransactionDate':
                            transaction.transaction_date = item.get('Value')
                
                transaction.save()
            
            return Response({
                'status': 'success',
                'message': 'Callback received'
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QueryStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, checkout_request_id):
        access_token = MPesaAuth.get_access_token()
        if not access_token:
            return Response({
                'error': 'Failed to authenticate with M-Pesa'
            }, status=status.HTTP_500_INTERNAL_SERVER_API)
        
        shortcode = settings.MPESA_SHORTCODE
        passkey = settings.MPESA_PASSKEY
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
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
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            return Response(response.json())
        except requests.RequestException as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TestAuthSuccessView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        return Response({
            'message': 'Test auth success',
            'status': 'ok'
        })
