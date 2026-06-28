from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()

@csrf_exempt
def get_token(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=400)
    
    try:
        body = json.loads(request.body)
        phone_number = body.get('phone_number', '')
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if not phone_number:
        return JsonResponse({'error': 'Phone number required'}, status=400)
    
    if phone_number.startswith('0'):
        phone_number = '254' + phone_number[1:]
    elif phone_number.startswith('+'):
        phone_number = phone_number[1:]
    
    user, created = User.objects.get_or_create(
        phone_number=phone_number
    )
    
    refresh = RefreshToken.for_user(user)
    
    return JsonResponse({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'user_id': user.id,
        'phone_number': phone_number,
        'is_new_user': created,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff
    })
