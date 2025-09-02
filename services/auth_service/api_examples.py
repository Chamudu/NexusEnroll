"""
API Usage Examples for NexusEnroll Authentication Service
Demonstrates how to interact with the authentication REST API
"""

# Example API calls using curl commands
# These can be run in a terminal when the service is running

api_examples = {
    "login": {
        "description": "Login with admin user",
        "method": "POST",
        "url": "http://127.0.0.1:5001/auth/login",
        "body": {
            "username": "admin",
            "password": "admin123"
        },
        "curl": '''curl -X POST -H "Content-Type: application/json" -d "{\\"username\\":\\"admin\\",\\"password\\":\\"admin123\\"}" http://127.0.0.1:5001/auth/login'''
    },
    
    "status": {
        "description": "Get service status",
        "method": "GET", 
        "url": "http://127.0.0.1:5001/auth/status",
        "curl": "curl http://127.0.0.1:5001/auth/status"
    },
    
    "create_user": {
        "description": "Create a new user",
        "method": "POST",
        "url": "http://127.0.0.1:5001/auth/users",
        "body": {
            "username": "new_student",
            "password": "password123",
            "email": "new@nexusenroll.edu",
            "role": "student"
        },
        "curl": '''curl -X POST -H "Content-Type: application/json" -d "{\\"username\\":\\"new_student\\",\\"password\\":\\"password123\\",\\"email\\":\\"new@nexusenroll.edu\\",\\"role\\":\\"student\\"}" http://127.0.0.1:5001/auth/users'''
    },
    
    "validate_session": {
        "description": "Validate session token (requires session token from login)",
        "method": "GET",
        "url": "http://127.0.0.1:5001/auth/validate",
        "headers": {
            "Authorization": "Bearer <session_token>"
        },
        "curl": '''curl -H "Authorization: Bearer <session_token>" http://127.0.0.1:5001/auth/validate'''
    },
    
    "list_users": {
        "description": "List all users (admin only, requires session token)",
        "method": "GET",
        "url": "http://127.0.0.1:5001/auth/users",
        "headers": {
            "Authorization": "Bearer <session_token>"
        },
        "curl": '''curl -H "Authorization: Bearer <session_token>" http://127.0.0.1:5001/auth/users'''
    },
    
    "authorize": {
        "description": "Check authorization for an action",
        "method": "POST",
        "url": "http://127.0.0.1:5001/auth/authorize",
        "headers": {
            "Authorization": "Bearer <session_token>"
        },
        "body": {
            "action": "manage_users"
        },
        "curl": '''curl -X POST -H "Authorization: Bearer <session_token>" -H "Content-Type: application/json" -d "{\\"action\\":\\"manage_users\\"}" http://127.0.0.1:5001/auth/authorize'''
    }
}

def print_api_examples():
    """Print all API examples with descriptions."""
    print("🔐 NexusEnroll Authentication Service API Examples")
    print("=" * 60)
    print()
    print("📋 Available API Endpoints:")
    print("-" * 30)
    
    for endpoint_name, details in api_examples.items():
        print(f"\n🔹 {endpoint_name.upper().replace('_', ' ')}")
        print(f"   Description: {details['description']}")
        print(f"   Method: {details['method']}")
        print(f"   URL: {details['url']}")
        
        if 'body' in details:
            print(f"   Body: {details['body']}")
        
        if 'headers' in details:
            print(f"   Headers: {details['headers']}")
        
        print(f"   Curl Command:")
        print(f"   {details['curl']}")
    
    print("\n" + "=" * 60)
    print("📝 Usage Instructions:")
    print("-" * 20)
    print("1. Start the authentication service: python main.py")
    print("2. Copy and paste the curl commands above into your terminal")
    print("3. Replace <session_token> with actual token from login response")
    print("4. The service runs on http://127.0.0.1:5001")
    print("\n🔧 PowerShell Alternative (Windows):")
    print("-" * 35)
    print("# Login example:")
    print('$body = @{username="admin"; password="admin123"} | ConvertTo-Json')
    print('Invoke-RestMethod -Uri "http://127.0.0.1:5001/auth/login" -Method POST -Body $body -ContentType "application/json"')
    
    print("\n# Status check:")
    print('Invoke-RestMethod -Uri "http://127.0.0.1:5001/auth/status"')

if __name__ == "__main__":
    print_api_examples()
