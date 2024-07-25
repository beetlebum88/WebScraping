from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Function to scrape information for a given country and save to a file
def scrape_country_info(driver, country, output_file):
    try:
        # Open the website for each country
        driver.get("https://www.starlink.com/")

        # Find the form elements using their HTML attributes
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='hero-service-input']"))
        )
        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mat-flat-button"))
        )

        # Input data into the form fields
        name_field.clear()
        name_field.send_keys(country)
        time.sleep(5)

        # Simulate pressing the "Arrow Up" key
        name_field.send_keys(Keys.ARROW_UP)
        time.sleep(5)

        # Simulate pressing the "Enter" key
        name_field.send_keys(Keys.ENTER)
        time.sleep(3)

        # Check if Starlink is not available in the area
        not_available_message = "Starlink is not available in your area."
        WebDriverWait(driver, 10).until_not(EC.text_to_be_present_in_element((By.TAG_NAME, 'p'), not_available_message))

        # Submit the form
        submit_button.click()

        # Explicit wait for the service details to be present
        service_details_present = EC.presence_of_element_located((By.CLASS_NAME, 'line-description'))
        WebDriverWait(driver, 20).until(service_details_present)
        time.sleep(20)

        # Collect the HTML content of the next page
        page_source = driver.page_source

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all divs with the specified attribute
        hardware_divs = soup.find_all('div', class_='line-description')

        # Iterate through the divs and find the Hardware value
        hardware_value = 'N/A'
        for hardware_div in hardware_divs:
            if 'Hardware' in hardware_div.get_text():
                value_element = hardware_div.find_next('div').find('div')
                hardware_value = value_element.text.strip() if value_element else 'N/A'
                break

        # Find all divs with the specified attribute
        deposit_div = soup.find('div', class_='ng-star-inserted', string='Deposit')
        service_div = soup.find('div', class_='line-description', string='Service')

        # Extract values for Deposit and Service
        deposit_value = deposit_div.find_next('div').find('span').text.strip() if deposit_div else 'N/A'
        service_value = service_div.find_next('div').find('span').text.strip() if service_div else 'N/A'

        # Save the results to the output file
        with open(output_file, 'a') as file:
            file.write(f"Country: {country}\n")
            file.write(f"Deposit: {deposit_value}\n")
            file.write(f"Service: {service_value}\n")
            file.write(f"Hardware: {hardware_value}\n")
            file.write("=" * 30 + "\n")

    except Exception as e:
        # Print an error message for the country
        print(f"Error processing {country}: {str(e)}")

        # Save the error message to the output file
        with open(output_file, 'a') as file:
            file.write(f"Country: {country}\n")
            file.write("No data or error\n")
            file.write("=" * 30 + "\n")

# Read countries from the file
with open('countries.txt', 'r') as file:
    countries = [line.strip() for line in file]

# Specify the output file
output_file = 'prices.txt'

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Iterate through the list of countries
for country in countries:
    scrape_country_info(driver, country, output_file)

# Close the browser window
driver.quit()
