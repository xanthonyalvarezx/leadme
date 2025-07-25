import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from geopy.geocoders import Nominatim

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Remove this to see the browser
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def save_to_database(data):
    """Save property managers to Laravel database via API"""
    api_url = "http://localhost:8000/api/property-managers"
    
    try:
        response = requests.post(api_url, json=data, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            print(f"   📊 Saved: {result.get('saved', 0)} | Skipped: {result.get('skipped', 0)} | Total: {result.get('total', 1)}")
            return True
        else:
            print(f"❌ Error saving to database: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        return False

def test_scrape_one_company():
    """Test scraping one company to verify the data flow"""
    driver = setup_driver()
    
    try:
        # Go to the search page
        search_url = "https://floridapropertymanagement.com/property-search/?thisSearchPage=HOME&search=Y&cat=834&zip=34101&submit="
        driver.get(search_url)
        time.sleep(3)
        
        print("Searching for 'Get Details' buttons...")
        
        # Find the first "Get Details" button
        get_details_buttons = driver.find_elements(By.CSS_SELECTOR, ".quote_container a")
        print(f"Found {len(get_details_buttons)} 'Get Details' buttons")
        
        if len(get_details_buttons) > 0:
            # Get the first company URL
            company_url = get_details_buttons[0].get_attribute("href")
            print(f"Company URL: {company_url}")
            
            # Open the company page
            driver.get(company_url)
            time.sleep(3)
            
            # Extract company information
            company_info = extract_company_details(driver)
            
            if company_info:
                print(f"✅ Extracted company info: {company_info}")
                
                # Save to database
                save_to_database([company_info])
                
                return company_info
            else:
                print("❌ Failed to extract company information")
                return None
        else:
            print("❌ No 'Get Details' buttons found")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    finally:
        driver.quit()

def extract_company_details(driver):
    """Extract company information from individual company page"""
    try:
        company_info = {
            "name": "",
            "phone": "",
            "address": "",
            "website": "",
            "yellowpages_profile": driver.current_url,
        }
        
        # Extract company name from the h1 tag
        try:
            name_element = driver.find_element(By.CSS_SELECTOR, ".agentdetail-info h1")
            company_info["name"] = name_element.text.strip()
            print(f"Found company name: {company_info['name']}")
        except:
            print("Could not find company name")
        
        # Extract contact information from the list items
        try:
            info_list = driver.find_element(By.CSS_SELECTOR, ".agentdetail-info ul")
            list_items = info_list.find_elements(By.TAG_NAME, "li")
            
            for item in list_items:
                text = item.text.strip()
                
                # Extract phone - looking for "Phone: 239-593-1233" format
                if "Phone:" in text:
                    phone_match = text.replace("Phone:", "").strip()
                    company_info["phone"] = phone_match
                    print(f"Found phone: {company_info['phone']}")
                
                # Extract address - looking for "Address: 4851 Tamiami Trail N, Suite 400 Naples, FL 34103 34101" format
                elif "Address:" in text:
                    address_match = text.replace("Address:", "").strip()
                    company_info["address"] = address_match
                    print(f"Found address: {company_info['address']}")
                    
                    # Extract city from address
                    city = extract_city_from_address(address_match)
                    company_info["city"] = city
                    print(f"Extracted city: {city}")
                
                # Extract website - looking for "Website: www.sentrymgt.com/offices/naples" format
                elif "Website:" in text:
                    try:
                        website_link = item.find_element(By.TAG_NAME, "a")
                        company_info["website"] = website_link.get_attribute("href")
                        print(f"Found website: {company_info['website']}")
                    except:
                        # Try to extract from text if no link
                        website_match = text.replace("Website:", "").strip()
                        company_info["website"] = website_match
                        print(f"Found website (text): {company_info['website']}")
        
        except Exception as e:
            print(f"Could not find contact information: {e}")
        
        company_info["type"] = "property_manager"
        
        return company_info if company_info["name"] else None
        
    except Exception as e:
        print(f"Error extracting company details: {e}")
        return None

def get_city_osm(address):
    """Get city name from address using OpenStreetMap geocoding"""
    try:
        geolocator = Nominatim(user_agent="city_extractor")
        time.sleep(1)  # Be respectful to the API
        location = geolocator.geocode(address)
        if location:
            rev = geolocator.reverse((location.latitude, location.longitude), language='en')
            address_dict = rev.raw.get("address", {})
            city = address_dict.get("city") or address_dict.get("town") or address_dict.get("village")
            print(f"Geocoded city for '{address}': {city}")
            return city
        else:
            print(f"Could not geocode address: {address}")
            return None
    except Exception as e:
        print(f"Error geocoding address '{address}': {e}")
        return None

def extract_city_from_address(address):
    """Extract city name from address string using geocoding"""
    print(f"Extracting city from address: {address}")
    
    # First try geocoding
    city = get_city_osm(address)
    if city:
        return city
    
    # Fallback to manual extraction if geocoding fails
    try:
        # Split address by commas
        parts = address.split(',')
        print(f"Address parts: {parts}")
        
        # Look for the city part (usually second to last part before state)
        if len(parts) >= 2:
            # The city is typically the second to last part before the state
            city_part = parts[-2].strip()
            print(f"City part before cleaning: {city_part}")
            
            # Remove any extra information like suite numbers, etc.
            # Look for common patterns
            if 'Suite' in city_part:
                # Split by 'Suite' and take the part after it
                suite_parts = city_part.split('Suite')
                if len(suite_parts) > 1:
                    city_part = suite_parts[1].strip()
                else:
                    city_part = suite_parts[0].strip()
            elif '#' in city_part:
                city_part = city_part.split('#')[0].strip()
            
            print(f"City part after cleaning: {city_part}")
            
            # Clean up any remaining extra text and get the last word (city name)
            words = city_part.split()
            print(f"Words in city part: {words}")
            
            if words:
                # Get the last word which should be the city name
                city_name = words[-1]
                print(f"Extracted city name: {city_name}")
                return city_name
            else:
                return ""
        else:
            return ""
    except Exception as e:
        print(f"Error extracting city from address '{address}': {e}")
        return ""

if __name__ == "__main__":
    print("🧪 Testing FPM Scraper - Single Company")
    print("=" * 50)
    
    result = test_scrape_one_company()
    
    if result:
        print(f"\n✅ Successfully scraped and saved: {result['name']}")
    else:
        print("\n❌ Failed to scrape company") 