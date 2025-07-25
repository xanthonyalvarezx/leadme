import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Define the cities to scrape
CITIES = [
    "Everglades City, FL",
    "Marco Island, FL", 
    "Naples, FL",
    "Bonita Springs",
"Cape Coral",
"Fort Myers",
"Sanibel",
"fort myers beach",
]

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Remove this to see the browser
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def save_to_database(data):
    """Save realtors to Laravel database via API"""
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

def scrape_realtors(location=""):
    driver = setup_driver()
    search_url = f"https://www.yellowpages.com/search?search_terms=realtors&geo_location_terms={location.replace(' ', '+')}"
    driver.get(search_url)

    all_results = []
    page = 1

    while True:
        print(f"Scraping page {page + 1}...")
        time.sleep(3)

        listings = driver.find_elements(By.CSS_SELECTOR, "div.result")

        for listing in listings:
            try:
                name = listing.find_element(By.CSS_SELECTOR, "a.business-name span").text.strip()
            except:
                name = ""

            try:
                phone = listing.find_element(By.CSS_SELECTOR, "div.phones.phone.primary").text.strip()
            except:
                phone = ""

            try:
                address = listing.find_element(By.CSS_SELECTOR, "p.adr").text.strip()
            except:
                address = ""

            try:
                website = listing.find_element(By.CSS_SELECTOR, "a.track-visit-website").get_attribute("href")
            except:
                website = ""

            try:
                biz_page = listing.find_element(By.CSS_SELECTOR, "a.business-name").get_attribute("href")
            except:
                biz_page = ""

            if name:  # Only add if we have at least a name
                all_results.append({
                    "name": name,
                    "phone": phone,
                    "address": address,
                    "website": website,
                    "yellowpages_profile": biz_page,
                    "city": location.split(',')[0].strip(),  # Extract city name from location
                    "type": "realtor"  # Mark as realtor
                })

        # Pagination
        try:
            next_btn = driver.find_element(By.LINK_TEXT, "Next")
            next_btn.click()
            page += 1
        except:
            print("No more pages or 'Next' button not found.")
            break

    driver.quit()
    return all_results

def scrape_all_cities():
    """Scrape realtors for all defined cities"""
    total_results = []
    
    for city in CITIES:
        print(f"\n🛠 Scraping realtors in {city}...")
        print("=" * 50)
        
        try:
            scraped_data = scrape_realtors(city)
            if scraped_data:
                print(f"📊 Found {len(scraped_data)} realtors in {city}")
                total_results.extend(scraped_data)
                
                # Save data for this city immediately
                save_to_database(scraped_data)
            else:
                print(f"❌ No data found for {city}")
                
        except Exception as e:
            print(f"❌ Error scraping {city}: {e}")
            continue
            
        # Add a delay between cities to be respectful to the server
        time.sleep(5)
    
    return total_results

if __name__ == "__main__":
    print("🚀 Starting Yellow Pages Realtor Scraper")
    print(f"📍 Cities to scrape: {', '.join(CITIES)}")
    print("=" * 60)
    
    all_scraped_data = scrape_all_cities()
    
    print("\n" + "=" * 60)
    print(f"🎉 Scraping completed!")
    print(f"📊 Total realtors found: {len(all_scraped_data)}")
    print("=" * 60) 