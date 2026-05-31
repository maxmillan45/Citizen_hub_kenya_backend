import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenhub.settings')
django.setup()

from accounts.otp_utils import generate_otp, store_otp, verify_otp

# Test OTP generation
otp = generate_otp()
print(f"Generated OTP: {otp}")

# Test storing and verifying
phone = "0712345678"
store_otp(phone, otp)
print(f"Stored OTP for {phone}")

# Test verification
is_valid = verify_otp(phone, otp)
print(f"OTP verification: {'PASS' if is_valid else 'FAIL'}")
