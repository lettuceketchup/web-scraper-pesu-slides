import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, deinit
from colors import task, success, error, info, info_cont

# Constants
DRIVER_PATH = './chromedriver.exe'

# Function to exit program
def exit_program(driver):
    '''Exit selenium_python program'''
    # Quit chromedriver
    driver.quit()

    # De-initialize colorama
    deinit()

# Initialize chromedriver
def initialize_driver():
    task("Initializing...")
    options = Options()
    options.add_argument('--log-level=3')
    options.add_argument("--window-size=1920,1200")
    options.headless = True # For headless mode

    try:
        task("\nStarting Browser...")
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        success("Started")
        return driver
    except:
        error("Could not start Browser")
        exit_program(driver)
        return None
