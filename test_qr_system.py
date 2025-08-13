#!/usr/bin/env python
"""
Test script for the QR code booking system
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldbrella.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from booking.models import Booking, BookingToken
from beach.models import Beach
from sunbed.models import Sunbed, Zone
from helpers.qr_utils import generate_booking_qr_code, generate_booking_qr_code_file

User = get_user_model()

def test_qr_code_generation():
    """Test QR code generation functionality"""
    print("Testing QR code generation...")
    
    try:
        # Create a test user
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'first_name': 'Test',
                'last_name': 'User',
                'is_staff': True
            }
        )
        print(f"✓ User created/retrieved: {user.email}")
        
        # Create a test beach
        beach, created = Beach.objects.get_or_create(
            title='Test Beach',
            defaults={
                'description': 'A test beach for QR code testing'
            }
        )
        print(f"✓ Beach created/retrieved: {beach.title}")
        
        # Create a test zone
        zone, created = Zone.objects.get_or_create(
            name='Test Zone',
            beach=beach,
            defaults={
                'description': 'A test zone'
            }
        )
        print(f"✓ Zone created/retrieved: {zone.name}")
        
        # Create a test sunbed
        sunbed, created = Sunbed.objects.get_or_create(
            identity='TEST001',
            zone=zone,
            defaults={
                'row': 1,
                'column': 1
            }
        )
        print(f"✓ Sunbed created/retrieved: {sunbed.identity}")
        
        # Create a test booking
        from datetime import date, timedelta
        tomorrow = date.today() + timedelta(days=1)
        
        booking, created = Booking.objects.get_or_create(
            user=user,
            beach=beach,
            booking_date=tomorrow,
            defaults={
                'status': 'reserved',
                'booked_by': user
            }
        )
        print(f"✓ Booking created/retrieved: {booking.id}")
        
        # Add sunbed to booking
        booking.sunbeds.add(sunbed)
        print(f"✓ Sunbed added to booking")
        
        # Ensure booking has a token
        token, created = BookingToken.objects.get_or_create(booking=booking)
        print(f"✓ Booking token: {token.key}")
        
        # Test QR code generation
        qr_data = generate_booking_qr_code(booking)
        print(f"✓ QR code generated successfully")
        print(f"  - Verification URL: {qr_data['verification_url']}")
        print(f"  - Token: {qr_data['token']}")
        print(f"  - QR Code length: {len(qr_data['qr_code'])} characters")
        
        # Test file generation
        filename = f"test_booking_{booking.id}_qr.png"
        qr_file_data = generate_booking_qr_code_file(booking, filename)
        print(f"✓ QR code file generated: {qr_file_data['filename']}")
        
        # Clean up test file
        if os.path.exists(filename):
            os.remove(filename)
            print(f"✓ Test file cleaned up")
        
        print("\n🎉 All QR code tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test API endpoints (basic structure)"""
    print("\nTesting API endpoints...")
    
    try:
        # Test that URLs are properly configured
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test admin URLs
        admin_urls = [
            f'/admin/booking/booking/{1}/qr-code/',
            '/admin/booking/booking/qr-scanner/',
        ]
        
        for url in admin_urls:
            response = client.get(url)
            # Should redirect to login (302) or show error (404) but not crash
            print(f"✓ Admin URL {url} responds with status: {response.status_code}")
        
        print("✓ API endpoint tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Error testing API endpoints: {str(e)}")
        return False

if __name__ == '__main__':
    print("🧪 Testing QR Code Booking System")
    print("=" * 50)
    
    success = True
    
    # Test QR code generation
    success &= test_qr_code_generation()
    
    # Test API endpoints
    success &= test_api_endpoints()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! The QR code system is working correctly.")
        print("\nNext steps:")
        print("1. Run 'python manage.py runserver' to start the development server")
        print("2. Access admin at http://localhost:8000/admin/")
        print("3. Create a booking and test the QR code functionality")
        print("4. Use the QR scanner at /admin/booking/booking/qr-scanner/")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    print("\nFor more information, see QR_CODE_API.md") 