from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import requests
import json

# Set your target Craigslist city
city = "lakeland"  # You can change to "sfbay", "losangeles", etc.

url = f"https://{city}.craigslist.org/search/lab?query=window+cleaner"

# Laravel API endpoint
LARAVEL_API_URL = "http://localhost:8000/api/jobs"

def send_job_to_laravel(title, details, link, posted_date):
    """Send job data to Laravel API"""
    try:
        data = {
            'title': title,
            'details': details,
            'link': link,
            'posted_date': posted_date
        }
        
        response = requests.post(LARAVEL_API_URL, json=data, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        if response.status_code == 201:
            print(f"✅ Job saved to database: {title[:50]}...")
            return True
        elif response.status_code == 409:
            print(f"⏭️ Job already exists: {title[:50]}...")
            return True  # Consider this a success since we don't want duplicates
        else:
            print(f"❌ Failed to save job: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending job to API: {e}")
        return False

options = Options()
driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=options
)

driver.get(url)
time.sleep(2)  # Wait for the page to load

print(f"\n🛠 Handyman Jobs in {city.capitalize()} Craigslist:\n")

# Process posts one by one to avoid stale element issues
post_count = 0
max_posts = 1500  # Limit to avoid too many requests

while post_count < max_posts:
    try:
        # Refresh the postings list each time
        postings = driver.find_elements(By.CLASS_NAME, "result-info")
        
        if post_count >= len(postings):
            print("No more posts to process")
            break
            
        # Get the current post
        current_post = postings[post_count]
        
        # Get the link element and job link from the correct anchor
        link_element = current_post.find_element(By.CSS_SELECTOR, "a.cl-search-anchor")
        job_link = link_element.get_attribute("href")
        
        # Try to get the date from the meta section span
        try:
            meta_section = current_post.find_element(By.CLASS_NAME, "meta")
            date_span = meta_section.find_element(By.TAG_NAME, "span")
            date_posted = date_span.get_attribute("title")
            print(f"Debug - Raw date string: {date_posted}")
            # Parse the date string and format it
            # Handle the full date format with time and timezone
            try:
                parsed_date = datetime.datetime.strptime(date_posted, "%a %b %d %Y %H:%M:%S GMT%z")
            except ValueError:
                # Try without timezone info
                parsed_date = datetime.datetime.strptime(date_posted.split(" GMT")[0], "%a %b %d %Y %H:%M:%S")
            
            formatted_date = parsed_date.strftime("%m/%d/%y")
            print(f"Date Posted: {formatted_date}")
        except Exception as e:
            print(f"Debug - Error parsing date: {e}")
            try:
                # Alternative: try to get the text content of the first span
                meta_section = current_post.find_element(By.CLASS_NAME, "meta")
                date_span = meta_section.find_element(By.TAG_NAME, "span")
                date_posted = date_span.text
                # For short format like "7/8", we'll just display it as is
                print(f"Date Posted: {date_posted} (short format)")
                formatted_date = date_posted
            except:
                print("Date Posted: Not available")
                formatted_date = "Unknown"
        
        link_element.click()
        
        # Wait for the new page to load
        time.sleep(3)
        
        # Now scrape details from the individual job posting page
        try:
            title = driver.find_element(By.ID, "titletextonly").text
            details = driver.find_element(By.ID, "postingbody").text
            
            # Get additional date information from the job posting page
            try:
                # Get the posted date from the job page
                posted_time = driver.find_element(By.CSS_SELECTOR, "p.postinginfo time.date")
                posted_date = posted_time.get_attribute("title")
                print(f"Job Page Posted Date: {posted_date}")
            except:
                print("Job Page Posted Date: Not available")
            
            # Try to get updated date if available
            try:
                updated_time = driver.find_elements(By.CSS_SELECTOR, "p.postinginfo time.date")[1]
                updated_date = updated_time.get_attribute("title")
                print(f"Job Page Updated Date: {updated_date}")
            except:
                print("Job Page Updated Date: Not available")
            
            print(f"Title: {title}")
            print(f"Details: {details[:200]}...")  # Truncate for display
            
            # Send job data to Laravel API
            send_job_to_laravel(title, details, job_link, formatted_date)
            
            print("-" * 50)
            
        except Exception as e:
            print(f"Error scraping job details: {e}")
        
        # Go back to the search results page
        driver.back()
        time.sleep(2)  # Wait for the page to load back
        
        post_count += 1
        
    except Exception as e:
        print(f"Error processing post {post_count + 1}: {e}")
        # Try to go back to search results if we're on a job page
        try:
            driver.back()
            time.sleep(2)
        except:
            # If that fails, reload the search page
            driver.get(url)
            time.sleep(2)
        post_count += 1

driver.quit()
