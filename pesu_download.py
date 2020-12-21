import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from colorama import init, deinit
from colors import task, success, error, info, info_cont
import pesu
from browser import initialize_driver, exit_program

# Define constants/paths
DOWNLOAD_PATH = './Slides/'

# Initialize colorama
init()

# Program Start Functions

# Download Slides
def download_slides(driver, subject='', subject_code=''):
    '''Downloads slides from PESU Academy'''
    pesu.connect(driver)
    pesu.login(driver)

# print('Start')
if __name__ == '__main__':
    # print('Starting')
    driver = initialize_driver()
    if(driver):
        download_slides(driver)

        # exit_program(driver)