from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()

@csrf_exempt
def generate_token(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            phone = body.get('phone_number', '254705632334')
        except:
            phone = '254705632334'
        
        # Create or get user
        user, created = User.objects.get_or_create(
            phone_number=phone,
            defaults={
                'username': phone,
                'phone_number': phone
            }
        )
        
        # Generate token
        refresh = RefreshToken.for_user(user)
        
        return JsonResponse({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_id': user.id,
            'phone_number': phone
        })
    
    return JsonResponse({'error': 'POST method required'}, status=400)
