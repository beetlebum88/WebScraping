import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()))

try:
    # Open the Marks and Spencer job search page
    driver.get('https://jobs.marksandspencer.com/job-search')

    # Wait for job listings to load (you can adjust the sleep time as needed)
    time.sleep(2)

    # Collect job titles and links from the first 2 pages
    job_data = []

    for page_num in range(2):  # Loop for 2 pages
        # Find all job listings
        job_listings = driver.find_elements(By.XPATH, '//div[contains(@class, "border-1")]')

        # Extract titles and links from each job listing
        for listing in job_listings:
            title_elem = listing.find_element(By.TAG_NAME, 'h3')
            title = title_elem.text.strip()

            link_elem = listing.find_element(By.XPATH, './/a[@data-track-trigger="job_listing_link"]')
            link = link_elem.get_attribute('href')

            job_data.append({
                'title': title,
                'url': link
            })

        # Navigate to the next page if available
        next_page_button = driver.find_element(By.XPATH, '//a[@aria-label="Page 2"]')
        if next_page_button:
            next_page_button.click()
            time.sleep(2)  # Wait for next page to load
        else:
            break

    # Save job data to a JSON file
    with open('job_data.json', 'w', encoding='utf-8') as f:
        json.dump(job_data, f, ensure_ascii=False, indent=4)

    print("Job data saved to job_data.json file.")

finally:
    # Quit the WebDriver session
    driver.quit()
