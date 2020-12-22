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
DOWNLOAD_PATH = './Downloads/'

# Initialize colorama
init()

# Program Start Functions

# Download Slides
def download(driver):
    '''Downloads slides from PESU Academy'''
    pesu.connect(driver) # Go to PESU Academy
    pesu.login(driver, default = 1) # Login
    subject_list = pesu.get_subject_list(driver)
    pesu.chose_subject(driver, subject_list)
    category = pesu.chose_category()
    units = pesu.choose_units(driver)
    for i in units:
        print(i)






if __name__ == '__main__':
    driver = initialize_driver()
    if(driver):
        download(driver)

        exit_program(driver)