import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Define the URL of the job search page
url = "https://www.workopolis.com/jobsearch/find-jobs?ak=software%20developer&l=Elmira%2C%20ON"
#url = "https://www.workopolis.com/jobsearch/find-jobs?ak=software%20developer&l=elmira%20ontario"

# Initialize ChromeDriver
driver_service = ChromeService(executable_path="C:\webdriver\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=driver_service)

# Navigate to the URL
driver.get(url)
print()
# Create a CSV file for saving job listings
filename =  "workopolis_" + datetime.now().strftime("%Y-%m-%d") + ".csv"
csv_filename = r"C:/Users/abdul/SENG8080-23F-Sec-1/Project Team 5/" + filename

#now you can open CSV and write to file
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Job Title', 'Company', 'Location', 'Estimated Salary']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    current_page = 1

    while True:
        try:
            # Find all job listings on the current page
            job_listings = driver.find_elements(By.CLASS_NAME, 'SerpJob')

            # Iterate through the job listings and write to CSV
            for job_listing in job_listings:
                try:
                    job_title = job_listing.find_element(By.CLASS_NAME, 'SerpJob-title').text.strip()
                except NoSuchElementException:
                    job_title = "N/A"

                try:
                    company = job_listing.find_element(By.CLASS_NAME, 'SerpJob-property.SerpJob-company').text.strip()
                except NoSuchElementException:
                    company = "N/A"

                try:
                    location = job_listing.find_element(By.CLASS_NAME, 'SerpJob-location').text.strip()
                except NoSuchElementException:
                    location = "N/A"

                try:
                    #salary = job_listing.find_element(By.CLASS_NAME, 'SalaryEstimate-value').text.strip()
                    estimated_salary_element = job_listing.find_elements(By.CLASS_NAME, 'Estimated_Salary')
                    salary_element = job_listing.find_elements(By.CLASS_NAME, 'Salary')
                    
                    # Use the first one found, or "N/A" if neither is found
                    if estimated_salary_element:
                        salary = estimated_salary_element[0].text.strip()
                    elif salary_element:
                        salary = salary_element[0].text.strip()
                    else:
                        salary = "N/A"
                except NoSuchElementException:
                    salary = "N/A"

                writer.writerow({'Job Title': job_title, 'Company': company, 'Location': location, 'Estimated Salary': salary})

            # Check if there is a next page
            next_button = driver.find_element(By.CSS_SELECTOR, '.Pagination-link--next')
            if 'disabled' in next_button.get_attribute('class'):
                print("No more pages to scrape. Exiting...")
                break
            else:
                print(f"Scraping page {current_page}")
                next_button.click()
                current_page += 1
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'SerpJob')))
        except TimeoutException:
            print("Timeout exception occurred. Continuing to the next page.")
        except StaleElementReferenceException:
            print("Stale element reference occurred. Retrying...")
        except Exception as e:
            print("An error occurred:", str(e))
            break

# Close the browser when done
driver.quit()

print(f"Job listings from {current_page} pages scraped and saved to {csv_filename}")
