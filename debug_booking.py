#!/usr/bin/env python
"""
Debug script to test booking creation and identify validation issues.
"""

import os
import sys
import django

# Setup Django first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldbrella.settings')
os.environ.setdefault('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver')
django.setup()

# Now import Django and DRF modules
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from beach.models import Beach
from sunbed.models import Sunbed
from zone.models import Zone
from location.models import Location

def debug_booking_creation():
    """Debug booking creation to identify validation issues."""
    
    # Create test data if it doesn't exist
    User = get_user_model()
    
    # Create test user
    user, created = User.objects.get_or_create(
        email='test@example.com',
        defaults={
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+1234567890',
            'is_active': True
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Create test location
    location, created = Location.objects.get_or_create(
        city='Test City',
        defaults={
            'country': 'US'
        }
    )
    
    # Create test beach
    beach, created = Beach.objects.get_or_create(
        title='Test Beach',
        defaults={
            'location': location,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'description': 'Test beach description'
        }
    )
    
    # Create test zone
    zone, created = Zone.objects.get_or_create(
        beach=beach,
        location='near_water'
    )
    
    # Create test sunbed
    sunbed, created = Sunbed.objects.get_or_create(
        zone=zone,
        defaults={
            'identity': 'TEST-001',
            'description': 'Test sunbed'
        }
    )
    
    # Create API client and authenticate
    client = APIClient()
    
    # Login to get token
    login_response = client.post('/api/v1/login', {
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.status_code}")
        print(login_response.data)
        return
    
    access_token = login_response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # Test booking creation with minimal data
    from datetime import date, timedelta
    
    booking_data = {
        'beach': beach.id,
        'booking_date': (date.today() + timedelta(days=1)).isoformat(),
        'user': user.id,
        'sunbeds': [sunbed.id]
    }
    
    print("Testing booking creation with data:")
    print(booking_data)
    
    response = client.post('/api/v1/bookings', booking_data, format='json')
    
    print(f"\nResponse status: {response.status_code}")
    print(f"Response data: {response.data}")
    
    if response.status_code == 400:
        print("\nValidation errors:")
        for field, errors in response.data.items():
            print(f"  {field}: {errors}")
    
    return response

if __name__ == "__main__":
    debug_booking_creation() 