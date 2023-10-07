import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Define the URL of the job search page
url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=software+developer&locationstring=Elmira%2C+ON"

# Initialize ChromeDriver
driver_service = ChromeService(executable_path="C:\webdriver\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=driver_service)

# Navigate to the URL
driver.get(url)

# Wait for the page to load (adjust the time as needed)
driver.implicitly_wait(10)

# Create a CSV file for saving job listings
csv_filename = r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/jobbank.csv"

# Create the necessary directory structure if it doesn't exist
os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

# Now you can open and write to the CSV file
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Job Title', 'Company', 'Location', 'Estimated Salary']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    current_page = 1

    while True:
        try:
            # Find all job listings on the current page
            job_listings = driver.find_elements(By.CSS_SELECTOR, '[id^="article-"]')

            # Iterate through the job listings and write to CSV
            for job_listing in job_listings:
                try:
                    job_title = job_listing.find_element(By.CLASS_NAME, 'noctitle').text.strip()
                except NoSuchElementException:
                    job_title = "N/A"

                try:
                    company = job_listing.find_element(By.CSS_SELECTOR, '.business').text.strip()
                except NoSuchElementException:
                    company = "N/A"

                try:
                    location = job_listing.find_element(By.CSS_SELECTOR, '.location').text.strip()
                except NoSuchElementException:
                    location = "N/A"

                try:
                    salary = job_listing.find_element(By.CSS_SELECTOR, '.salary').text.strip()
                except NoSuchElementException:
                    salary = "N/A"

                # Replace unwanted characters and whitespace
                job_title = job_title.replace('\n', ' ').replace('\r', '')
                company = company.replace('\n', ' ').replace('\r', '')
                location = location.replace('\n', ' ').replace('\r', '')
                salary = salary.replace('\n', ' ').replace('\r', '')

                writer.writerow({'Job Title': job_title, 'Company': company, 'Location': location, 'Estimated Salary': salary})

            # Find the "Show More Results" button by its "id" attribute
            show_more_button = driver.find_element(By.ID, 'moreresultbutton')

            if not show_more_button.is_enabled():
                break  # No more pages to scrape

            # Scroll to the "Show More Results" button to make it clickable
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)
            show_more_button.click()
            current_page += 1

            # Add a delay to allow the new listings to load (adjust as needed)
            time.sleep(5)
        except NoSuchElementException:
            print("No 'Show More Results' button found. Exiting...")
            break
        except Exception as e:
            print("An error occurred:", str(e))
            break

# Close the browser when done
driver.quit()

print(f"Job listings from {current_page} pages scraped and saved to {csv_filename}")
