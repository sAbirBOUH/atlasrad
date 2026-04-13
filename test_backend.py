import requests
import json

def test_backend():
    url = "http://127.0.0.1:8000/api/auth/register/"
    payload = {
        "username": "testuser_sabir",
        "email": "test@atlasrad.com",
        "password": "SecurePass@123",
        "password_confirm": "SecurePass@123",
        "first_name": "Test",
        "last_name": "User",
        "hospital": "Test Hospital",
        "specialty": "Radiology"
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        print(f"Connecting to {url}...")
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 201:
            print("\n✅ Registration Success!")
        else:
            print("\n❌ Registration Failed (Check if user already exists)")
            
    except Exception as e:
        print(f"\n❌ Error connecting to server: {e}")
        print("Check if 'python manage.py runserver' is actually running.")

if __name__ == "__main__":
    test_backend()
