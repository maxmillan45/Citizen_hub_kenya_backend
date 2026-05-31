from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer
from .otp_utils import (
    generate_otp, send_otp_via_sms, store_otp, verify_otp,
    get_otp_attempts, increment_otp_attempts, reset_otp_attempts
)

class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_exists = User.objects.filter(phone_number=phone_number).exists()
        
        attempts = get_otp_attempts(phone_number)
        if attempts >= 3:
            return Response({
                'error': 'Too many OTP requests. Please try again later.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        otp_code = generate_otp()
        sms_sent = send_otp_via_sms(phone_number, otp_code)
        
        if sms_sent:
            store_otp(phone_number, otp_code)
            increment_otp_attempts(phone_number)
            return Response({
                'message': 'OTP sent successfully',
                'phone_number': phone_number,
                'user_exists': user_exists
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Failed to send OTP. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp_code = request.data.get('otp_code')
        
        if not phone_number or not otp_code:
            return Response({
                'error': 'Phone number and OTP code are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not verify_otp(phone_number, otp_code):
            return Response({
                'error': 'Invalid or expired OTP code'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'is_active': True}
        )
        
        reset_otp_attempts(phone_number)
        
        return Response({
            'message': 'OTP verified successfully',
            'user': UserSerializer(user).data,
            'is_new_user': created
        }, status=status.HTTP_200_OK)


class CompleteLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        
        phone_number = request.data.get('phone_number')
        
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(phone_number=phone_number)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
