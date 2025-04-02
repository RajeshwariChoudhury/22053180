import requests

# --- REGISTRATION API ---
def register():
    registration_url = "http://20.244.56.144/evaluation-service/register"
    
    registration_data = {
        "email": "22053180@kiit.ac.in",  # Replace with your college email
        "name": "Rajeshwari Choudhury",
        "mobileNo": "9064952434",
        "githubUsername": "RajeshwariChoudhury",  # Must match GitHub
        "rollNo": "22053180",  # Must match university records
        "collegeName": "Kalinga Institute of Industrial Technology",
        "accessCode": "nwpwrZ"  # From your email (NOT the example)
    }

    response = requests.post(registration_url, json=registration_data)
    
    if response.status_code == 200:
        print("Registration Successful!")
        print("Response:", response.json())
        return response.json()  # Contains clientID & clientSecret
    else:
        print("Registration Failed!")
        print("Status Code:", response.status_code)
        print("Error:", response.text)
        return None

# --- AUTHENTICATION API ---
def get_auth_token(client_id, client_secret):
    auth_url = "http://20.244.56.144/evaluation-service/auth"
    
    auth_data = {
        "email": "22053180@kiit.ac.in",  # Same as registration
        "name": "Rajeshwari Choudhury",
        "rollNo": "22053180",
        "accessCode": "nwpwrZ",  # Same as registration
        "clientID": client_id,
        "clientSecret": client_secret
    }

    response = requests.post(auth_url, json=auth_data)
    
    if response.status_code == 200:
        print("\nAuthentication Successful!")
        print("Token:", response.json())
        return response.json()["access_token"]  # Extract Bearer token
    else:
        print("\nAuthentication Failed!")
        print("Status Code:", response.status_code)
        print("Error:", response.text)
        return None

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Step 1: Register (only once)
    registration_response = register()
    
    if registration_response:
        # Step 2: Get Auth Token (using clientID & clientSecret from registration)
        client_id = registration_response["clientID"]
        client_secret = registration_response["clientSecret"]
        
        auth_token = get_auth_token(client_id, client_secret)
        
        # Save token for future API calls
        if auth_token:
            print("\nSUCCESS! Use this token in headers for authenticated requests:")
            print(f"Authorization: Bearer {auth_token}")