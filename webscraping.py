from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Setup Selenium WebDriver (Ensure chromedriver is in the PATH or specify the path to chromedriver)
driver = webdriver.Chrome()  # Specify path if necessary, e.g., webdriver.Chrome(executable_path='/path/to/chromedriver')

# URL of the webpage to scrape
url = "https://www.yearupalumni.org/s/1841/interior.aspx?sid=1841&gid=2&pgid=440"  # Replace with the actual URL
driver.get(url)

print("Page loaded successfully.")

# Wait for the page to load completely (adjust to a real class name or other valid element)
try:
    WebDriverWait(driver, 70).until(
        EC.presence_of_element_located((By.CLASS_NAME, "post-title")))  # Adjust with a valid class
    print("Page loaded successfully")
except Exception as e:
    print(f"Error while waiting for page load: {e}")
    driver.quit()

# Check the page source to see if elements are being loaded
print(driver.page_source)  # Add this line to print the full page source for debugging

# Get the page source after JavaScript content is loaded
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Debug: Print the prettified HTML (for troubleshooting)
# print(soup.prettify())  # Uncomment this line if you need to inspect the HTML structure

# Extract data from specific elements, adjust the 'post-title' and 'post-link' based on actual structure
data = []
for item in soup.find_all('div', class_='blog-post'):  # Adjust based on actual structure
    title = item.find('h2', class_='post-title').text.strip() if item.find('h2', class_='post-title') else 'No title'
    link = item.find('a')['href'] if item.find('a') else 'No link'
    print(f"Title: {title}, Link: {link}")  # Debug print
    data.append({'Title': title, 'Link': link})

# Save the data to CSV if data is found
if data:
    df = pd.DataFrame(data)
    df.to_csv('scraped_data.csv', index=False)
    print("Data saved to scraped_data.csv")
else:
    print("No data found!")

# Read the CSV file and display it in the terminal
df = pd.read_csv('scraped_data.csv')
print("Scraped Data from CSV:")
print(df)

# Close the browser after scraping
driver.quit()
