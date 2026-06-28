from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json

User = get_user_model()

@csrf_exempt
def make_superuser(request):
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
    
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    user.is_superuser = True
    user.is_staff = True
    user.save()
    
    return JsonResponse({
        'success': True,
        'message': f'User {phone_number} is now a superuser',
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff
    })
