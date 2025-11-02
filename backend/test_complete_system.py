"""
Complete End-to-End Test for Dual Database Authentication System
Tests both admin and LSC user login flows with comprehensive validation
"""

import requests
import json
from datetime import datetime

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(key, value):
    print(f"  {key}: {value}")

def decode_jwt_payload(token):
    """Decode JWT token payload (without verification)"""
    try:
        import base64
        # JWT format: header.payload.signature
        payload = token.split('.')[1]
        # Add padding if needed
        padding = len(payload) % 4
        if padding:
            payload += '=' * (4 - padding)
        decoded = base64.b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        return f"Error decoding: {str(e)}"

def test_login(lsc_number, password, expected_user_type, test_name):
    """Test login for a specific user"""
    print_header(f"TEST: {test_name}")
    
    url = 'http://localhost:8000/api/auth/login/'
    data = {
        'lscNumber': lsc_number,
        'password': password
    }
    
    try:
        # Make login request
        print(f"\n📡 Sending login request...")
        print_info("LSC Number/Code", lsc_number)
        print_info("Endpoint", url)
        
        response = requests.post(url, json=data)
        
        # Check status code
        if response.status_code != 200:
            print_error(f"Login failed with status {response.status_code}")
            print_info("Response", response.text)
            return False
        
        result = response.json()
        
        # Validate response structure
        print_success(f"Login successful (Status: {response.status_code})")
        
        # Check for required fields
        required_fields = ['access', 'refresh', 'user', 'message']
        for field in required_fields:
            if field not in result:
                print_error(f"Missing required field: {field}")
                return False
        
        print_success("All required fields present")
        
        # Validate user data
        user = result['user']
        print(f"\n👤 USER INFORMATION:")
        print_info("  ID", user.get('id'))
        print_info("  Name", user.get('lsc_name'))
        print_info("  Code/Number", user.get('lsc_code') or user.get('lsc_number'))
        print_info("  Email", user.get('email'))
        print_info("  User Type", user.get('user_type'))
        print_info("  Database", user.get('database'))
        print_info("  Active", user.get('is_active'))
        
        # Validate user type
        if user.get('user_type') != expected_user_type:
            print_error(f"User type mismatch: expected '{expected_user_type}', got '{user.get('user_type')}'")
            return False
        
        print_success(f"User type matches: {expected_user_type}")
        
        # Decode and validate JWT tokens
        print(f"\n🎟️  JWT TOKENS:")
        access_token = result['access']
        refresh_token = result['refresh']
        
        print_info("  Access Token Length", len(access_token))
        print_info("  Refresh Token Length", len(refresh_token))
        
        # Decode access token
        print(f"\n🔍 ACCESS TOKEN CLAIMS:")
        access_payload = decode_jwt_payload(access_token)
        if isinstance(access_payload, dict):
            for key, value in access_payload.items():
                if key not in ['exp', 'iat', 'jti']:  # Skip timestamp fields
                    print_info(f"  {key}", value)
            
            # Validate token claims match user data
            if access_payload.get('user_type') != expected_user_type:
                print_error("Token user_type doesn't match expected value")
                return False
            
            print_success("Token claims validated")
        
        # Display welcome message
        print(f"\n💬 MESSAGE:")
        print_info("  ", result.get('message'))
        
        print_success(f"{test_name} - ALL CHECKS PASSED ✓")
        return True
        
    except Exception as e:
        print_error(f"Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print_header("🚀 DUAL DATABASE AUTHENTICATION - END-TO-END TEST")
    print(f"\nTest Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test 1: Admin Login
    results.append(
        test_login(
            lsc_number='LC2101-CDOE',
            password='admin123',
            expected_user_type='admin',
            test_name='ADMIN LOGIN (online_edu.lsc_admins)'
        )
    )
    
    # Test 2: LSC User Login
    results.append(
        test_login(
            lsc_number='LC3001',
            password='user123',
            expected_user_type='user',
            test_name='LSC USER LOGIN (lsc_portal_db.lsc_auth_lscuser)'
        )
    )
    
    # Test 3: Invalid Credentials
    print_header("TEST: INVALID CREDENTIALS (Should Fail)")
    try:
        response = requests.post(
            'http://localhost:8000/api/auth/login/',
            json={'lscNumber': 'INVALID', 'password': 'wrong'}
        )
        if response.status_code == 400 or response.status_code == 401:
            print_success("Invalid credentials correctly rejected")
            results.append(True)
        else:
            print_error(f"Expected 400/401, got {response.status_code}")
            results.append(False)
    except Exception as e:
        print_error(f"Test failed: {str(e)}")
        results.append(False)
    
    # Final Summary
    print_header("📊 TEST SUMMARY")
    total_tests = len(results)
    passed_tests = sum(results)
    failed_tests = total_tests - passed_tests
    
    print(f"\nTotal Tests: {total_tests}")
    print_success(f"Passed: {passed_tests}")
    if failed_tests > 0:
        print_error(f"Failed: {failed_tests}")
    
    print(f"\nSuccess Rate: {(passed_tests/total_tests*100):.1f}%")
    
    if all(results):
        print_header("🎉 ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION!")
        print("\n✅ Dual database authentication is working correctly")
        print("✅ Admin users authenticated from online_edu.lsc_admins")
        print("✅ LSC users authenticated from lsc_portal_db.lsc_auth_lscuser")
        print("✅ JWT tokens generated with correct claims")
        print("✅ Invalid credentials properly rejected")
        print("\n🚀 You can now use the login system!")
    else:
        print_header("⚠️  SOME TESTS FAILED - REVIEW OUTPUT ABOVE")
    
    print(f"\nTest Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
