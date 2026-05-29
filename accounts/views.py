from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.utils import timezone
import logging
from .models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check rate limit
        ip = request.META.get('REMOTE_ADDR')
        rate_key = f'register_{ip}'
        attempts = cache.get(rate_key, 0)
        
        if attempts >= 3:
            return Response({'error': 'Too many registration attempts. Try again later.'}, 
                          status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(phone_number=phone_number)
            cache.set(rate_key, attempts + 1, timeout=3600)
            logger.info(f'New user registered: {phone_number}')
            
            return Response({
                'message': 'User registered successfully',
                'phone_number': user.phone_number
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f'Registration failed: {str(e)}')
            return Response({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check rate limit
        ip = request.META.get('REMOTE_ADDR')
        rate_key = f'login_{ip}'
        attempts = cache.get(rate_key, 0)
        
        if attempts >= 5:
            return Response({'error': 'Too many login attempts. Try again later.'}, 
                          status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        try:
            user = User.objects.get(phone_number=phone_number)
            refresh = RefreshToken.for_user(user)
            
            # Update last active
            user.last_active = timezone.now()
            user.save(update_fields=['last_active'])
            
            cache.set(rate_key, attempts + 1, timeout=1800)
            logger.info(f'User logged in: {phone_number}')
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
        except User.DoesNotExist:
            cache.set(rate_key, attempts + 1, timeout=1800)
            logger.warning(f'Failed login attempt for non-existent user: {phone_number}')
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ProfileView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = request.user
        if 'language' in request.data:
            user.language = request.data['language']
            user.save()
            logger.info(f'User {user.phone_number} updated language to {user.language}')
        return Response(UserSerializer(user).data)
