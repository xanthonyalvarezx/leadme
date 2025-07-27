import requests
import json

def test_api_connection():
    """Test if the API is working"""
    try:
        # Test the check endpoint
        response = requests.post("http://localhost:8000/api/property-managers/check", 
                               json={"name": "Test Company"}, 
                               headers={'Content-Type': 'application/json'})
        print(f"Check endpoint status: {response.status_code}")
        print(f"Check endpoint response: {response.json()}")
        
        # Test the save endpoint
        test_data = [{
            "name": "Test Property Manager",
            "phone": "555-123-4567",
            "address": "123 Test Street, Naples, FL 34101",
            "website": "http://test.com",
            "yellowpages_profile": "http://test-profile.com",
            "city": "Naples",
            "type": "property_manager"
        }]
        
        response = requests.post("http://localhost:8000/api/property-managers", 
                               json=test_data, 
                               headers={'Content-Type': 'application/json'})
        print(f"Save endpoint status: {response.status_code}")
        print(f"Save endpoint response: {response.json()}")
        
        return True
    except Exception as e:
        print(f"Error testing API: {e}")
        return False

if __name__ == "__main__":
    print("Testing FPM scraper API connection...")
    test_api_connection() 