import requests
import time

BACKEND_URL = "http://localhost:8000"

def smoke_test():
    print(f"Attempting to connect to backend at {BACKEND_URL}...")
    # Give the backend a moment to start up
    time.sleep(5) 
    try:
        response = requests.get(BACKEND_URL)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Smoke test successful! Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Smoke test failed: {e}")
        exit(1)

if __name__ == "__main__":
    smoke_test() 