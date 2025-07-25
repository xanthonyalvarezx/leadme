import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from geopy.geocoders import Nominatim

# Define the cities to scrape
ZIP_CODES = [
    "34101", "34102", "34103", "34104", "34105", 
    "34106", "34107", "34108", "34109", "34110", 
    "34112", "34113", "34114", "34116", "34117", 
    "34119", "34120", "34137", "34138", "34139", 
    "34140", "34141", "34142", "34143", "34145", 
    "34146","33901", "33902", "33903", "33904", 
    "33905", "33906", "33907", "33908", "33909", 
    "33910", "33911", "33912", "33913", "33914", 
    "33915", "33916", "33917", "33918", "33919", 
    "33920", "33921", "33922", "33924", "33928", 
    "33931", "33932", "33936", "33945", "33956", 
    "33957", "33970", "33971", "33972", "33973", 
    "33974", "33976", "33990", "33991", "33993", 
    "33994", "34133", "34134", "34135", "34136"]

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Remove this to see the browser
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def save_to_database(data):
    """Save property managers to Laravel database via API with duplicate checking"""
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

def check_company_exists(company_name):
    """Check if a company already exists in the database"""
    api_url = "http://localhost:8000/api/property-managers/check"
    
    try:
        response = requests.post(api_url, json={"name": company_name}, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        if response.status_code == 200:
            result = response.json()
            return result.get('exists', False)
        else:
            print(f"❌ Error checking company existence: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking company existence: {e}")
        return False

def scrape_property_managers(zip=""):
    driver = setup_driver()
    search_url = f"https://floridapropertymanagement.com/property-search/?thisSearchPage=HOME&search=Y&cat=834&zip={zip}&submit="
    driver.get(search_url)

    all_results = []
    page = 1

    while True:
        print(f"Scraping page {page}...")
        time.sleep(3)

        # Find all "Get Details" buttons
        get_details_buttons = driver.find_elements(By.CSS_SELECTOR, ".quote_container a")
        print(f"Found {len(get_details_buttons)} 'Get Details' buttons on page {page}")

        for i, button in enumerate(get_details_buttons, 1):
            try:
                print(f"Processing company {i}/{len(get_details_buttons)} on page {page}")
                
                # Get the URL from the button
                company_url = button.get_attribute("href")
                if not company_url:
                    print("No URL found for this button, skipping...")
                    continue
                
                print(f"Company URL: {company_url}")
                
                # Open the company page in a new tab
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(company_url)
                time.sleep(3)
                
                # Extract company information from the detail page
                company_info = extract_company_details(driver)
                
                if company_info:
                    # Check if company already exists in database
                    if check_company_exists(company_info['name']):
                        print(f"⏭️ Skipping {company_info['name']} - already exists in database")
                        continue
                    
                    # Use the extracted city from address, fallback to zip if no city found
                    if not company_info.get("city"):
                        company_info["city"] = zip
                    company_info["type"] = "property_manager"
                    all_results.append(company_info)
                    print(f"✅ Extracted: {company_info['name']} from {company_info['city']}")
                else:
                    print("❌ Failed to extract company information")
                
                # Close the tab and go back to the listing page
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error processing company {i}: {e}")
                # Make sure we're back on the main page
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                continue

        # Pagination
        try:
            next_btn = driver.find_element(By.LINK_TEXT, "Next")
            next_btn.click()
            page += 1
            time.sleep(3)
        except:
            print("No more pages or 'Next' button not found.")
            break

    driver.quit()
    return all_results

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
                print(f"Processing list item: {text}")
                
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
        
        # Print final extracted data
        print(f"Extracted company info: {company_info}")
        
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
    # First try geocoding
    city = get_city_osm(address)
    if city:
        return city
    
    # Fallback to manual extraction if geocoding fails
    try:
        # Split address by commas
        parts = address.split(',')
        
        # Look for the city part (usually second to last part before state)
        if len(parts) >= 2:
            # The city is typically the second to last part before the state
            city_part = parts[-2].strip()
            
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
            
            # Clean up any remaining extra text and get the last word (city name)
            words = city_part.split()
            if words:
                # Get the last word which should be the city name
                city_name = words[-1]
                return city_name
            else:
                return ""
        else:
            return ""
    except Exception as e:
        print(f"Error extracting city from address '{address}': {e}")
        return ""

def scrape_all_zip_codes():
    """Scrape property managers for all defined zip codes"""
    total_results = []
    
    for zip in ZIP_CODES:
        print(f"\n🛠 Scraping property managers in {zip}...")
        print("=" * 50)
        
        try:
            scraped_data = scrape_property_managers(zip)
            if scraped_data:
                print(f"📊 Found {len(scraped_data)} property managers in {zip}")
                total_results.extend(scraped_data)
                
                # Save data for this city immediately
                save_to_database(scraped_data)
            else:
                print(f"❌ No data found for {zip}")
                
        except Exception as e:
            print(f"❌ Error scraping {zip}: {e}")
            continue
            
        # Add a delay between cities to be respectful to the server
        time.sleep(5)
    
    return total_results

if __name__ == "__main__":
    print("🚀 Starting Property Manager Scraper")
    print(f"📍 Zip Codes to scrape: {', '.join(ZIP_CODES)}")
    print("=" * 60)
    
    all_scraped_data = scrape_all_zip_codes()
    
    print("\n" + "=" * 60)
    print(f"🎉 Scraping completed!")
    print(f"📊 Total property managers found: {len(all_scraped_data)}")
    print("=" * 60)
