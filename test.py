import requests
import base64
from config import CLIENT_ID, CLIENT_SECRET  # Import credentials

# Function to get the access token
def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    
    # Encode credentials
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    # Make request to get access token
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an error if request fails

    return response.json().get("access_token")

# Get the access token
access_token = get_access_token()

# Define the API endpoint
url = "https://api.spotify.com/v1/recommendations"

# Define the parameters
params = {
    "seed_tracks": "0lYBSQXN6rCTvUZvg9S0lU",  # Replace with your track ID
    #"limit": 1,  # Number of recommendations
    #"market": "GB"  # Change if needed
}

# Set the headers with the correct Bearer token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Make the API request
response = requests.get(url, headers=headers, params=params)

# Check if request was successful
if response.status_code == 200:
    recommendations = response.json()
    for track in recommendations["tracks"]:
        print(f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
else:
    print("Error:", response.status_code, response.text)
