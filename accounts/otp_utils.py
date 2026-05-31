import random
from django.core.cache import cache

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_sms(phone_number, otp_code):
    # Development mode - always print to console
    print(f"\n{'='*50}")
    print(f"OTP VERIFICATION CODE")
    print(f"Phone: {phone_number}")
    print(f"Code: {otp_code}")
    print(f"{'='*50}\n")
    return True

def store_otp(phone_number, otp_code):
    cache_key = f"otp_{phone_number}"
    cache.set(cache_key, otp_code, timeout=300)
    return True

def verify_otp(phone_number, user_otp):
    cache_key = f"otp_{phone_number}"
    stored_otp = cache.get(cache_key)
    if stored_otp and stored_otp == user_otp:
        cache.delete(cache_key)
        return True
    return False

def get_otp_attempts(phone_number):
    attempts_key = f"otp_attempts_{phone_number}"
    return cache.get(attempts_key, 0)

def increment_otp_attempts(phone_number):
    attempts_key = f"otp_attempts_{phone_number}"
    attempts = cache.get(attempts_key, 0)
    cache.set(attempts_key, attempts + 1, timeout=600)
    return attempts + 1

def reset_otp_attempts(phone_number):
    attempts_key = f"otp_attempts_{phone_number}"
    cache.delete(attempts_key)
