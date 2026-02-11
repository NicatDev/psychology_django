import os
import django
import sys

# Django mühitini quraşdırırıq
sys.path.append('c:/Users/Boss/OneDrive/Desktop/psychology_django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from authApp.models import VerificationCode

User = get_user_model()
client = APIClient()

def test_password_reset():
    print("Testing Password Reset Flow...")

    # 1. Test istifadəçisi yaradırıq
    email = "test_reset@example.com"
    password = "SafePassword123!"
    user, created = User.objects.get_or_create(email=email)
    user.set_password(password)
    user.save()
    print(f"User created: {email}")

    # 2. Forgot Password sorğusu göndəririk
    print("\nSending Forgot Password Request...")
    response = client.post('/auth/forgot-password/', {'email': email}, format='json')
    print(f"Status: {response.status_code}")
    if hasattr(response, 'data'):
        print(f"Response: {response.data}")
    else:
        print(f"Response Content: {response.content}")
    
    if response.status_code != 200:
        print("FAILED: Forgot Password Request")
        return

    # 3. Kodu bazadan alırıq
    code_obj = VerificationCode.objects.filter(user=user).last()
    if not code_obj:
        print("FAILED: Code not generated")
        return
    code = code_obj.code
    print(f"Code retrieved from DB: {code}")

    # 4. Yanlış kodla yoxlayırıq
    print("\nTesting Invalid Code...")
    response = client.post('/auth/reset-password/', {
        'email': email,
        'code': '000000',
        'new_password': 'NewSafePassword123!'
    }, format='json')
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print("SUCCESS: Invalid code rejected")
    else:
        print("FAILED: Invalid code accepted")

    # 5. Doğru kodla şifrəni yeniləyirik
    print("\nResetting Password...")
    new_password = "NewSafePassword123!"
    response = client.post('/auth/reset-password/', {
        'email': email,
        'code': code,
        'new_password': new_password
    }, format='json')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.data}")

    if response.status_code == 200:
        print("SUCCESS: Password reset successful")
        
        # 6. Yeni şifrə ilə login olmağı yoxlayırıq
        user.refresh_from_db()
        if user.check_password(new_password):
             print("SUCCESS: User can login with new password")
        else:
             print("FAILED: Password mismatch in DB")
    else:
        print("FAILED: Password reset failed")

    # Təmizlik
    user.delete()

if __name__ == "__main__":
    test_password_reset()
