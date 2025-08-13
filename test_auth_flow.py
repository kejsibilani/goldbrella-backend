import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldbrella.settings')
django.setup()

from rest_framework.test import APIClient


def test_auth_flow():
    client = APIClient()
    print("\n--- Testing Sign Up (Register) ---")
    register_data = {
        "email": "testuser1@example.com",
        "password": "Testpass123!",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+1234567890",
        "address": "Test Address",
        "preferred_language": "en",
        "role": "guest"
    }
    resp = client.post("/api/v1/register", register_data, format="json")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.data}")
    if resp.status_code not in [200, 201]:
        print("Sign up failed!")
        return

    print("\n--- Testing Sign In (Login) ---")
    login_data = {
        "email": register_data["email"],
        "password": register_data["password"]
    }
    resp = client.post("/api/v1/login", login_data, format="json")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.data}")
    if resp.status_code != 200 or "access" not in resp.data:
        print("Sign in failed!")
        return
    access = resp.data["access"]
    refresh = resp.data["refresh"]

    print("\n--- Testing Sign Out (Logout) ---")
    resp = client.post("/api/v1/logout", {"refresh": refresh}, format="json")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.data}")
    if resp.status_code not in [200, 205]:
        print("Sign out failed!")
        return

    print("\nAll authentication flows passed!")

if __name__ == "__main__":
    test_auth_flow() 