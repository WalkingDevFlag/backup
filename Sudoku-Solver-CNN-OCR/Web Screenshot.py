from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set the path to the Brave browser
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"  # Change this to your Brave browser path

# Set the options to use the Brave browser
options = Options()
options.binary_location = brave_path
options.add_argument("--start-maximized")

# Set the path to the ChromeDriver
webdriver_path = "C:\\Program Files\\chrome-win64\\chromedriver.exe"  # Change this to your ChromeDriver path

# Set the directory to save the screenshot
save_directory = "E:\\Sid Folder\\Random Python Scripts\\"

# Initialize the driver
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the website
driver.get("https://sudoku.com/")

# Allow some time for the page to load
time.sleep(5)

# Take a screenshot and save it to the specified directory
screenshot_path = save_directory + "sudoku_screenshot.png"
driver.save_screenshot(screenshot_path)

# Close the browser
driver.quit()

print(f"Screenshot saved successfully at: {screenshot_path}")
