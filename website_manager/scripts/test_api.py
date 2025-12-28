import requests

BASE_URL = "http://127.0.0.1:5000"
SITE_ID = "plumber123"

def send_test_enquiry():
    payload = {
        "name": "John",
        "email": "john@test.com",
        "message": "Need a boiler repair ASAP"
    }

    response = requests.post(
        f"{BASE_URL}/api/enquiry/{SITE_ID}",
        json=payload
    )

    print("Status code:", response.status_code)
    print("Response:", response.json())


if __name__ == "__main__":
    send_test_enquiry()
