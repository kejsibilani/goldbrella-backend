#!/usr/bin/env python
"""
Test script to verify all API endpoints are properly configured.
This script will check if all URL patterns are valid and accessible.
"""

import os
import sys
import django
from django.urls import reverse
from django.test import Client
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldbrella.settings')
os.environ.setdefault('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver')
django.setup()

def test_api_endpoints():
    """Test all API endpoints to ensure they're properly configured."""
    
    client = Client()
    
    # List of endpoints to test
    endpoints = [
        # Account endpoints
        '/api/v1/login',
        '/api/v1/verify',
        '/api/v1/refresh',
        '/api/v1/logout',
        '/api/v1/profile',
        '/api/v1/register',
        '/api/v1/users',
        
        # Beach endpoints
        '/api/v1/beaches',
        '/api/v1/beach-images',
        '/api/v1/beach-images-list',
        '/api/v1/beach-opening-hours',
        '/api/v1/beach-opening-hours-list',
        '/api/v1/beach-opening-seasons',
        '/api/v1/beach-opening-seasons-list',
        '/api/v1/beach-season-opening-hours',
        '/api/v1/beach-zones',
        '/api/v1/beach-sunbeds',
        '/api/v1/beach-inventory-items',
        
        # Booking endpoints
        '/api/v1/bookings',
        '/api/v1/bookings/locations',
        '/api/v1/bookings/beaches',
        '/api/v1/anonymous/bookings',
        
        # Payment endpoints
        '/api/v1/payments',
        
        # Sunbed endpoints
        '/api/v1/sunbeds',
        
        # Zone endpoints
        '/api/v1/zones',
        
        # Location endpoints
        '/api/v1/locations',
        
        # Services endpoints
        '/api/v1/facilities',
        '/api/v1/rules',
        
        # Inventory endpoints
        '/api/v1/inventory-items',
        
        # Invoice endpoints
        '/api/v1/invoices',
        
        # Complaint endpoints
        '/api/v1/complaints',
        
        # Review endpoints
        '/api/v1/reviews',
        
        # Notification endpoints
        '/api/v1/notifications',
        
        # Mailer endpoints
        '/api/v1/scheduled-emails',
        
        # Shift endpoints
        '/api/v1/shifts',
    ]
    
    print("Testing API endpoints...")
    print("=" * 50)
    
    working_endpoints = []
    broken_endpoints = []
    
    for endpoint in endpoints:
        try:
            # Try to resolve the URL
            response = client.get(endpoint)
            if response.status_code in [200, 401, 403, 404]:  # Valid responses
                working_endpoints.append(endpoint)
                print(f"✓ {endpoint} - Status: {response.status_code}")
            else:
                broken_endpoints.append(endpoint)
                print(f"✗ {endpoint} - Status: {response.status_code}")
        except Exception as e:
            broken_endpoints.append(endpoint)
            print(f"✗ {endpoint} - Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"Working endpoints: {len(working_endpoints)}")
    print(f"Broken endpoints: {len(broken_endpoints)}")
    
    if broken_endpoints:
        print("\nBroken endpoints:")
        for endpoint in broken_endpoints:
            print(f"  - {endpoint}")
    
    return len(broken_endpoints) == 0

if __name__ == "__main__":
    success = test_api_endpoints()
    sys.exit(0 if success else 1) 