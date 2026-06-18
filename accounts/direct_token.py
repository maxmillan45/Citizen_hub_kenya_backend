from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()

@csrf_exempt
def get_token_direct(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number', '254705632334')
        except:
            phone_number = '254705632334'
        
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'username': phone_number}
        )
        
        refresh = RefreshToken.for_user(user)
        
        return JsonResponse({
            'success': True,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_id': user.id
        })
    
    return JsonResponse({'error': 'POST required'}, status=400)
