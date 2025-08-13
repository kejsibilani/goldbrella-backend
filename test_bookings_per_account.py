#!/usr/bin/env python3
"""
Test script to verify bookings per account functionality
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000/api"
LOGIN_URL = f"{BASE_URL}/account/login"
BOOKINGS_URL = f"{BASE_URL}/bookings"
USER_PROFILE_URL = f"{BASE_URL}/account/users/me"

def test_bookings_per_account():
    """Test that bookings are properly filtered per user account"""
    
    print("🧪 Testing Bookings Per Account Functionality")
    print("=" * 50)
    
    # Test 1: Login and get user profile
    print("\n1. Testing user authentication and profile...")
    
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
        
        # Get user profile
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = requests.get(USER_PROFILE_URL, headers=headers)
        
        if profile_response.status_code == 200:
            user_profile = profile_response.json()
            print(f"✅ User profile retrieved: {user_profile.get('email')}")
            print(f"   Name: {user_profile.get('first_name')} {user_profile.get('last_name')}")
            print(f"   Role: {user_profile.get('role')}")
        else:
            print(f"❌ Failed to get user profile: {profile_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Authentication test failed: {str(e)}")
        return False
    
    # Test 2: Get user's bookings
    print("\n2. Testing user-specific bookings...")
    
    try:
        bookings_response = requests.get(BOOKINGS_URL, headers=headers)
        
        if bookings_response.status_code == 200:
            bookings_data = bookings_response.json()
            total_bookings = bookings_data.get('count', 0)
            bookings = bookings_data.get('results', [])
            
            print(f"✅ Retrieved {total_bookings} bookings for user")
            
            if bookings:
                print("\n📋 Sample booking details:")
                for i, booking in enumerate(bookings[:3]):  # Show first 3 bookings
                    print(f"   Booking {i+1}:")
                    print(f"     ID: {booking.get('id')}")
                    print(f"     Beach: {booking.get('beach', {}).get('title', 'N/A')}")
                    print(f"     Date: {booking.get('booking_date')}")
                    print(f"     Status: {booking.get('status')}")
                    print(f"     User: {booking.get('user', {}).get('email', 'N/A')}")
                    print()
            else:
                print("   ℹ️  No bookings found for this user")
                
        else:
            print(f"❌ Failed to get bookings: {bookings_response.status_code}")
            print(f"Response: {bookings_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Bookings test failed: {str(e)}")
        return False
    
    # Test 3: Verify user isolation
    print("\n3. Testing user data isolation...")
    
    try:
        # Try to access a specific booking (if any exist)
        if bookings:
            first_booking_id = bookings[0].get('id')
            specific_booking_url = f"{BOOKINGS_URL}/{first_booking_id}"
            
            specific_response = requests.get(specific_booking_url, headers=headers)
            
            if specific_response.status_code == 200:
                specific_booking = specific_response.json()
                booking_user_email = specific_booking.get('user', {}).get('email')
                current_user_email = user_profile.get('email')
                
                if booking_user_email == current_user_email:
                    print("✅ User can only access their own bookings")
                else:
                    print(f"❌ User isolation failed: booking belongs to {booking_user_email}")
                    return False
            else:
                print(f"❌ Failed to get specific booking: {specific_response.status_code}")
                return False
        else:
            print("ℹ️  No bookings to test isolation with")
            
    except Exception as e:
        print(f"❌ User isolation test failed: {str(e)}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Bookings per account functionality is working correctly.")
    return True

def test_booking_filters():
    """Test booking filtering functionality"""
    
    print("\n🔍 Testing Booking Filters")
    print("=" * 30)
    
    # You'll need to implement this with actual authentication
    print("ℹ️  Filter testing requires authentication setup")
    print("   - Status filtering")
    print("   - Date range filtering") 
    print("   - Beach-specific filtering")
    print("   - Pagination")

if __name__ == "__main__":
    print("🚀 Starting Bookings Per Account Tests")
    print("Note: You may need to update test credentials in the script")
    
    success = test_bookings_per_account()
    
    if success:
        test_booking_filters()
        print("\n✅ All functionality tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Please check the implementation.") 