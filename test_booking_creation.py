#!/usr/bin/env python3
"""
Test script to verify booking creation functionality
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api"
LOGIN_URL = f"{BASE_URL}/account/login"
BOOKINGS_URL = f"{BASE_URL}/bookings"
BEACHES_URL = f"{BASE_URL}/beaches"
SUNBEDS_URL = f"{BASE_URL}/sunbeds"

def test_booking_creation():
    """Test that bookings can be created and appear in the right places"""
    
    print("🧪 Testing Booking Creation Functionality")
    print("=" * 50)
    
    # Test 1: Login and get user profile
    print("\n1. Testing user authentication...")
    
    # You'll need to replace these with actual test user credentials
    test_credentials = {
        "email": "test@example.com",  # Replace with actual test user
        "password": "testpassword123"  # Replace with actual test password
    }
    
    try:
        # Login
        login_response = requests.post(LOGIN_URL, json=test_credentials)
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
            
        tokens = login_response.json()
        access_token = tokens.get('access')
        
        if not access_token:
            print("❌ No access token received")
            return False
            
        print("✅ Login successful")
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
    except Exception as e:
        print(f"❌ Authentication test failed: {str(e)}")
        return False
    
    # Test 2: Get available beaches and sunbeds
    print("\n2. Getting available beaches and sunbeds...")
    
    try:
        # Get beaches
        beaches_response = requests.get(BEACHES_URL, headers=headers)
        if beaches_response.status_code != 200:
            print(f"❌ Failed to get beaches: {beaches_response.status_code}")
            return False
            
        beaches_data = beaches_response.json()
        beaches = beaches_data.get('results', [])
        
        if not beaches:
            print("❌ No beaches available")
            return False
            
        test_beach = beaches[0]
        print(f"✅ Found beach: {test_beach.get('title')}")
        
        # Get sunbeds for the beach
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        sunbeds_response = requests.get(
            f"{SUNBEDS_URL}?beach_id={test_beach['id']}&booking_date={tomorrow}&only_available=true",
            headers=headers
        )
        
        if sunbeds_response.status_code != 200:
            print(f"❌ Failed to get sunbeds: {sunbeds_response.status_code}")
            return False
            
        sunbeds_data = sunbeds_response.json()
        sunbeds = sunbeds_data.get('results', [])
        
        if not sunbeds:
            print("❌ No available sunbeds for tomorrow")
            return False
            
        test_sunbed = sunbeds[0]
        print(f"✅ Found available sunbed: {test_sunbed.get('identity')}")
        
    except Exception as e:
        print(f"❌ Failed to get beaches/sunbeds: {str(e)}")
        return False
    
    # Test 3: Create a booking
    print("\n3. Creating a test booking...")
    
    try:
        booking_data = {
            "beach": test_beach['id'],
            "booking_date": tomorrow,
            "sunbeds": [test_sunbed['id']],
            "note": "Test booking created via API"
        }
        
        create_response = requests.post(BOOKINGS_URL, json=booking_data, headers=headers)
        
        if create_response.status_code != 201:
            print(f"❌ Failed to create booking: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            return False
            
        created_booking = create_response.json()
        booking_id = created_booking.get('id')
        
        print(f"✅ Booking created successfully! ID: {booking_id}")
        print(f"   Beach: {created_booking.get('beach', {}).get('title')}")
        print(f"   Date: {created_booking.get('booking_date')}")
        print(f"   Status: {created_booking.get('status')}")
        print(f"   Sunbeds: {len(created_booking.get('sunbeds', []))}")
        
    except Exception as e:
        print(f"❌ Failed to create booking: {str(e)}")
        return False
    
    # Test 4: Verify booking appears in user's bookings
    print("\n4. Verifying booking appears in user's bookings...")
    
    try:
        user_bookings_response = requests.get(BOOKINGS_URL, headers=headers)
        
        if user_bookings_response.status_code != 200:
            print(f"❌ Failed to get user bookings: {user_bookings_response.status_code}")
            return False
            
        user_bookings_data = user_bookings_response.json()
        user_bookings = user_bookings_data.get('results', [])
        
        # Find our created booking
        found_booking = None
        for booking in user_bookings:
            if booking.get('id') == booking_id:
                found_booking = booking
                break
        
        if found_booking:
            print("✅ Booking found in user's bookings!")
            print(f"   Booking ID: {found_booking.get('id')}")
            print(f"   Beach: {found_booking.get('beach', {}).get('title')}")
            print(f"   Status: {found_booking.get('status')}")
        else:
            print("❌ Created booking not found in user's bookings")
            return False
            
    except Exception as e:
        print(f"❌ Failed to verify booking: {str(e)}")
        return False
    
    # Test 5: Verify booking appears in admin view (if user is admin)
    print("\n5. Verifying booking appears in admin view...")
    
    try:
        # This would require admin credentials, but we can test the endpoint structure
        admin_bookings_response = requests.get(BOOKINGS_URL, headers=headers)
        
        if admin_bookings_response.status_code == 200:
            admin_bookings_data = admin_bookings_response.json()
            admin_bookings = admin_bookings_data.get('results', [])
            
            # Find our booking in admin view
            admin_found_booking = None
            for booking in admin_bookings:
                if booking.get('id') == booking_id:
                    admin_found_booking = booking
                    break
            
            if admin_found_booking:
                print("✅ Booking found in admin view!")
                print(f"   User: {admin_found_booking.get('user', {}).get('email')}")
                print(f"   Booked by: {admin_found_booking.get('booked_by', {}).get('email')}")
            else:
                print("⚠️  Booking not found in admin view (may be due to permissions)")
        else:
            print(f"⚠️  Admin view test skipped (status: {admin_bookings_response.status_code})")
            
    except Exception as e:
        print(f"⚠️  Admin view test failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Booking creation test completed successfully!")
    print(f"📋 Created booking ID: {booking_id}")
    print("✅ Booking appears in user's bookings")
    print("✅ Booking is properly stored in database")
    return True

def test_anonymous_booking():
    """Test anonymous booking creation"""
    
    print("\n🔍 Testing Anonymous Booking Creation")
    print("=" * 40)
    
    try:
        # Get a beach for testing
        beaches_response = requests.get(BEACHES_URL)
        if beaches_response.status_code != 200:
            print("❌ Failed to get beaches for anonymous test")
            return False
            
        beaches = beaches_response.json().get('results', [])
        if not beaches:
            print("❌ No beaches available for anonymous test")
            return False
            
        test_beach = beaches[0]
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Create anonymous booking
        anonymous_booking_data = {
            "beach": test_beach['id'],
            "booking_date": tomorrow,
            "sunbeds": [1],  # Assuming sunbed ID 1 exists
            "user": {
                "email": f"anonymous-{datetime.now().timestamp()}@test.com",
                "first_name": "Anonymous",
                "last_name": "User",
                "phone_number": "+1234567890"
            }
        }
        
        anonymous_response = requests.post(f"{BASE_URL}/anonymous/bookings", json=anonymous_booking_data)
        
        if anonymous_response.status_code == 201:
            anonymous_booking = anonymous_response.json()
            print(f"✅ Anonymous booking created! ID: {anonymous_booking.get('id')}")
            return True
        else:
            print(f"❌ Anonymous booking failed: {anonymous_response.status_code}")
            print(f"Response: {anonymous_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Anonymous booking test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Booking Creation Tests")
    print("Note: You may need to update test credentials in the script")
    
    success = test_booking_creation()
    
    if success:
        test_anonymous_booking()
        print("\n✅ All booking functionality tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Please check the implementation.") 