import requests
import json

print("\n" + "="*60)
print("Testing LSC User Login: LC3001")
print("="*60)

url = 'http://localhost:8000/api/auth/login/'
data = {
    'lscNumber': 'LC3001',
    'password': 'user123'
}

try:
    response = requests.post(url, json=data)
    print(f"\n📡 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ LOGIN SUCCESS!")
        print("\n" + "="*60)
        print("USER INFORMATION:")
        print("="*60)
        if 'user' in result:
            user = result['user']
            print(f"👤 LSC Name: {user.get('lsc_name', 'N/A')}")
            print(f"🏢 LSC Number: {user.get('lsc_number', 'N/A')}")
            print(f"📧 Email: {user.get('email', 'N/A')}")
            print(f"📊 User Type: {user.get('user_type', 'N/A')}")
            print(f"💾 Database: {user.get('database', 'N/A')}")
            print(f"✓ Active: {user.get('is_active', 'N/A')}")
        
        print("\n" + "="*60)
        print("JWT TOKENS:")
        print("="*60)
        if 'access' in result:
            print(f"🎟️  Access Token: {result['access'][:50]}...")
        if 'refresh' in result:
            print(f"🔄 Refresh Token: {result['refresh'][:50]}...")
        
        if 'message' in result:
            print(f"\n💬 Message: {result['message']}")
        
        print("\n" + "="*60)
        print("FULL RESPONSE:")
        print("="*60)
        print(json.dumps(result, indent=2))
    else:
        print(f"\n❌ LOGIN FAILED")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
