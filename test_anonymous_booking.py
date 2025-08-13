#!/usr/bin/env python
"""
Test script for anonymous booking functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldbrella.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from beach.models import Beach
from sunbed.models import Sunbed, Zone
from datetime import date, timedelta
import json

User = get_user_model()

def test_anonymous_booking():
    """Test anonymous booking creation"""
    print("Testing anonymous booking creation...")
    
    try:
        # Create test data
        user, created = User.objects.get_or_create(
            email='test_anon@example.com',
            defaults={
                'first_name': 'Test',
                'last_name': 'Anonymous',
                'role': 'guest'
            }
        )
        print(f"✓ Test user created/retrieved: {user.email}")
        
        beach, created = Beach.objects.get_or_create(
            title='Test Beach for Anonymous',
            defaults={
                'description': 'A test beach for anonymous booking testing'
            }
        )
        print(f"✓ Test beach created/retrieved: {beach.title}")
        
        zone, created = Zone.objects.get_or_create(
            name='Test Zone for Anonymous',
            beach=beach,
            defaults={
                'description': 'A test zone for anonymous bookings'
            }
        )
        print(f"✓ Test zone created/retrieved: {zone.name}")
        
        sunbed, created = Sunbed.objects.get_or_create(
            identity='ANON001',
            zone=zone,
            defaults={
                'row': 1,
                'column': 1
            }
        )
        print(f"✓ Test sunbed created/retrieved: {sunbed.identity}")
        
        # Test data for anonymous booking
        tomorrow = date.today() + timedelta(days=1)
        booking_data = {
            'user': {
                'email': 'anonymous@example.com',
                'first_name': 'Anonymous',
                'last_name': 'User',
                'phone_number': '+1234567890'
            },
            'sunbeds': [sunbed.id],
            'booking_date': tomorrow.isoformat(),
            'note': 'Test anonymous booking'
        }
        
        print(f"✓ Test data prepared")
        print(f"  - User: {booking_data['user']['email']}")
        print(f"  - Beach: {beach.title}")
        print(f"  - Sunbed: {sunbed.identity}")
        print(f"  - Date: {tomorrow}")
        
        # Test the API endpoint
        client = Client()
        
        # Test anonymous booking creation
        response = client.post(
            '/api/v1/anonymous/bookings',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        print(f"✓ API response status: {response.status_code}")
        
        if response.status_code == 201:
            print("🎉 Anonymous booking created successfully!")
            booking_response = response.json()
            print(f"  - Booking ID: {booking_response.get('id')}")
            print(f"  - Status: {booking_response.get('status')}")
            return True
        else:
            print(f"❌ Anonymous booking failed with status {response.status_code}")
            print(f"Response: {response.content.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🧪 Testing Anonymous Booking System")
    print("=" * 50)
    
    success = test_anonymous_booking()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Anonymous booking test passed!")
        print("\nThe anonymous booking system is working correctly.")
    else:
        print("❌ Anonymous booking test failed.")
        print("\nPlease check the error messages above.")
    
    print("\nYou can now test the anonymous booking through your frontend application.") 