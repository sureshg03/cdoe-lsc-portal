#!/usr/bin/env python
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_toggle_status():
    """Test the toggle status functionality"""
    session_id = 1

    print("Testing toggle status functionality...")
    print("-" * 50)

    # First, get current status
    try:
        response = requests.get(f'{BASE_URL}/application-settings/{session_id}/')
        print(f"GET response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Response data keys: {list(data.keys())}")
            print(f"Current status: {data.get('status')}")
            print(f"is_open: {data.get('is_open')}")
            print(f"is_close: {data.get('is_close')}")
        else:
            print(f"Failed to get session: {response.status_code}")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"Error getting session: {e}")
        return

    print("\nTesting toggle...")
    try:
        response = requests.post(f'{BASE_URL}/application-settings/{session_id}/toggle_status/')
        print(f"POST response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Message: {data.get('message')}")
            session_data = data.get('data', {})
            print(f"New status: {session_data.get('status')}")
            print(f"New is_open: {session_data.get('is_open')}")
            print(f"New is_close: {session_data.get('is_close')}")
        else:
            print(f"Toggle failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error toggling status: {e}")

if __name__ == '__main__':
    test_toggle_status()