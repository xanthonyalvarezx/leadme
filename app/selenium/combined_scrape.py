import time
import requests
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re

# Define the cities to scrape
CITIES = [
    "Everglades City, FL",
    "Marco Island, FL", 
    "Naples, FL",
    "Bonita Springs",
"Cape Coral"
"Fort Myers"
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
    """Save leads to Laravel database via API"""
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

def scrape_leads(location="", search_type="property+managers", lead_type="property_manager"):
    driver = setup_driver()
    search_url = f"https://www.yellowpages.com/search?search_terms={search_type}&geo_location_terms={location.replace(' ', '+')}"
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
                address = listing.find_element(By.CSS_SELECTOR, "div.adr").text.strip()
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
                    "type": lead_type
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

def scrape_florida_property_management():
    """Scrape Florida Property Management directory using the new method"""
    from FPM_scrape import scrape_property_managers, ZIP_CODES
    
    all_companies = []
    
    # Use a subset of zip codes for the combined scraper to avoid taking too long
    # You can modify this list as needed
    selected_zips = ["34101", "34102", "34103", "34104", "34105", "34106", "34107", "34108", "34109", "34110"]
    
    print(f"Scraping Florida Property Management for {len(selected_zips)} zip codes...")
    
    for zip_code in selected_zips:
        print(f"\nScraping zip code: {zip_code}")
        try:
            companies = scrape_property_managers(zip_code)
            if companies:
                all_companies.extend(companies)
                print(f"Found {len(companies)} companies in {zip_code}")
                
                # Save data for this zip code immediately
                save_to_database(companies)
            else:
                print(f"No companies found in {zip_code}")
                
        except Exception as e:
            print(f"Error scraping {zip_code}: {e}")
            continue
            
        # Add delay between zip codes
        time.sleep(3)
    
    return all_companies

def get_company_links_from_directory(driver, directory_url):
    """Get all company links from a directory listing page"""
    try:
        driver.get(directory_url)
        time.sleep(3)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "directory-section"))
        )
        
        company_links = []
        
        # Find all company links
        try:
            # Look for links in directory sections
            directory_sections = driver.find_elements(By.CLASS_NAME, "directory-section")
            
            for section in directory_sections:
                try:
                    # Find company name links
                    links = section.find_elements(By.CSS_SELECTOR, "h2 a, .cs-post-title h2 a")
                    for link in links:
                        href = link.get_attribute("href")
                        if href and "directory" in href:
                            company_links.append(href)
                except:
                    continue
            
            # Also look for any other company links on the page
            all_links = driver.find_elements(By.TAG_NAME, "a")
            for link in all_links:
                href = link.get_attribute("href")
                if href and "directory" in href and href not in company_links:
                    company_links.append(href)
        
        except NoSuchElementException:
            print(f"Could not find company links on {directory_url}")
        
        return list(set(company_links))  # Remove duplicates
        
    except TimeoutException:
        print(f"Timeout waiting for directory page to load: {directory_url}")
        return []
    except Exception as e:
        print(f"Error getting company links from {directory_url}: {str(e)}")
        return []

def extract_company_info(driver, url):
    """Extract company information from a single company page"""
    try:
        driver.get(url)
        time.sleep(3)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "agentinfo-detail"))
        )
        
        company_info = {
            'name': '',
            'phone': '',
            'website': '',
            'address': '',
            'city': '',
            'state': '',
            'zip': '',
            'type': 'Property Manager'
        }
        
        # Extract company name
        try:
            name_element = driver.find_element(By.CSS_SELECTOR, ".agentdetail-info h1")
            company_info['name'] = name_element.text.strip()
        except NoSuchElementException:
            print(f"Could not find company name on {url}")
        
        # Extract contact information from the list
        try:
            info_list = driver.find_element(By.CSS_SELECTOR, ".agentdetail-info ul")
            list_items = info_list.find_elements(By.TAG_NAME, "li")
            
            for item in list_items:
                text = item.text.strip()
                
                # Extract phone
                if "Phone:" in text:
                    phone_match = re.search(r'Phone:\s*(.+)', text)
                    if phone_match:
                        company_info['phone'] = phone_match.group(1).strip()
                
                # Extract address
                elif "Address:" in text:
                    address_match = re.search(r'Address:\s*(.+)', text)
                    if address_match:
                        full_address = address_match.group(1).strip()
                        company_info['address'] = full_address
                        
                        # Parse city, state, zip from address
                        address_parts = full_address.split(',')
                        if len(address_parts) >= 2:
                            # Extract city
                            city_part = address_parts[-2].strip()
                            company_info['city'] = city_part
                            
                            # Extract state and zip from last part
                            state_zip_part = address_parts[-1].strip()
                            state_zip_match = re.search(r'([A-Z]{2})\s+(\d{5})', state_zip_part)
                            if state_zip_match:
                                company_info['state'] = state_zip_match.group(1)
                                company_info['zip'] = state_zip_match.group(2)
                
                # Extract website
                elif "Website:" in text:
                    try:
                        website_link = item.find_element(By.TAG_NAME, "a")
                        company_info['website'] = website_link.get_attribute("href")
                    except NoSuchElementException:
                        # Try to extract from text if no link
                        website_match = re.search(r'Website:\s*(.+)', text)
                        if website_match:
                            company_info['website'] = website_match.group(1).strip()
        
        except NoSuchElementException:
            print(f"Could not find contact information on {url}")
        
        return company_info
        
    except TimeoutException:
        print(f"Timeout waiting for page to load: {url}")
        return None
    except Exception as e:
        print(f"Error extracting info from {url}: {str(e)}")
        return None

def scrape_all_cities_and_types():
    """Scrape both property managers and realtors for all defined cities"""
    total_results = []
    
    # Define scraping tasks
    scraping_tasks = [
        {"search_type": "property+managers", "lead_type": "property_manager", "name": "Property Managers"},
        {"search_type": "realtors", "lead_type": "realtor", "name": "Realtors"}
    ]
    
    for task in scraping_tasks:
        print(f"\n{'='*60}")
        print(f"Starting {task['name']} Scraping")
        print(f"{'='*60}")
        
        task_total = 0
        
        for city in CITIES:
            print(f"\nScraping {task['name'].lower()} in {city}...")
            print("-" * 50)
            
            try:
                scraped_data = scrape_leads(city, task['search_type'], task['lead_type'])
                if scraped_data:
                    print(f"Found {len(scraped_data)} {task['name'].lower()} in {city}")
                    total_results.extend(scraped_data)
                    task_total += len(scraped_data)
                    
                    # Save data for this city immediately
                    save_to_database(scraped_data)
                else:
                    print(f"No data found for {city}")
                    
            except Exception as e:
                print(f"Error scraping {city}: {e}")
                continue
                
            # Add a delay between cities to be respectful to the server
            time.sleep(5)
        
        print(f"\n{task['name']} scraping completed: {task_total} total found")
    
    return total_results

if __name__ == "__main__":
    print("Starting Combined Lead Scraper")
    print("Sources: Yellow Pages + Florida Property Management Directory")
    print(f"Cities to scrape: {', '.join(CITIES)}")
    print("Types to scrape: Property Managers & Realtors")
    print("=" * 60)
    
    all_scraped_data = []
    
    # First scrape Yellow Pages
    print("\n🌐 Starting Yellow Pages Scraping...")
    yellow_pages_data = scrape_all_cities_and_types()
    all_scraped_data.extend(yellow_pages_data)
    
    # Then scrape Florida Property Management Directory
    print("\n🏠 Starting Florida Property Management Directory Scraping...")
    florida_data = scrape_florida_property_management()
    
    # Convert Florida data to match Yellow Pages format
    for company in florida_data:
        converted_company = {
            "name": company['name'],
            "phone": company['phone'],
            "address": company['address'],
            "website": company['website'],
            "yellowpages_profile": company.get('yellowpages_profile', ''),  # Use yellowpages_profile from FPM scraper
            "city": company['city'],
            "type": company['type']
        }
        all_scraped_data.append(converted_company)
    
    # Note: Florida data is already saved to database in the scrape_florida_property_management function
    
    print("\n" + "=" * 60)
    print(f"All scraping completed!")
    print(f"Yellow Pages leads: {len(yellow_pages_data)}")
    print(f"Florida Directory leads: {len(florida_data)}")
    print(f"Total leads found: {len(all_scraped_data)}")
    print("=" * 60) 