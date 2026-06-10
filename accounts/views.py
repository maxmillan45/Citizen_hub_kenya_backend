from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(phone_number=phone_number)
        
        return Response({
            'message': 'User registered successfully',
            'phone_number': user.phone_number
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = request.user
        if 'language' in request.data:
            user.language = request.data['language']
            user.save()
        if 'notification_preferences' in request.data:
            # Add notification preferences to user model
            pass
        return Response(UserSerializer(user).data)
    
    def delete(self, request):
        """Delete user account - Data Protection Act compliance"""
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ChangePhoneView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        new_phone = request.data.get('new_phone_number')
        if not new_phone:
            return Response({'error': 'New phone number required'}, status=400)
        
        if User.objects.filter(phone_number=new_phone).exists():
            return Response({'error': 'Phone number already in use'}, status=400)
        
        user = request.user
        user.phone_number = new_phone
        user.save()
        
        return Response({'message': 'Phone number updated successfully'})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception:
            return Response({'message': 'Logged out successfully'})
