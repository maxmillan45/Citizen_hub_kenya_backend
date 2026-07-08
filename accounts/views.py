from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer
import requests
import base64
from datetime import datetime
from django.conf import settings

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data.get('phone_number'),
                password=serializer.validated_data.get('password')
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception:
            return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone_number = request.data.get('phone_number')
        try:
            user = User.objects.get(phone_number=phone_number)
            return Response({'message': 'Password reset link sent'})
        except User.DoesNotExist:
            return Response({'message': 'If account exists, reset link sent'}, status=status.HTTP_200_OK)

class TestAuthSuccessView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        return Response({"message": "Test auth success", "status": "ok"})

class CompleteProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        language = request.data.get('language')
        
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if language:
            user.language = language
        
        user.save()
        
        return Response({
            'message': 'Profile completed successfully',
            'user': UserSerializer(user).data
        })

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
            # Query transaction status
            from accounts.mpesa_views import MPesaAuth, QueryStatusView
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
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
