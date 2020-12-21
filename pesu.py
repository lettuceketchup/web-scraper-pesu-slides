import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from colorama import init, deinit
from colors import task, success, error, info, info_cont, enter
from browser import exit_program

# Constants
URL = 'https://pesuacademy.com/'
LOGINS = 'logins.csv'

# Functions
# Connect to database
def connect(driver):
    '''Connect to PESU Academy'''
    try:
        task("\nConnecting to PESU Academy...")
        driver.get(URL)
        success("Connected")
        try:
            task('Page Loading...')
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@id="postloginform#/Academy/j_spring_security_check"]'))
            )
            success('Page Loaded')
        except:
            error('Page not loaded')
    except:
        error("Could not connect to PESU Academy")
        exit_program(driver)

def enter_login():
    '''Enter login details'''
    task('\nEnter login details')
    usn = enter('USN: ')
    password  = enter('Password: ')
    return usn, password

def login_credentials():
    '''Check for saved login details'''
    logins = []
    try:
        # Open file
        f = open(LOGINS, 'r', encoding='utf-8')
        # Extract logins
        csv_reader = csv.reader(f, delimiter=',')
        for entry in csv_reader:
            if(len(entry) == 0):
                continue
            logins.append(entry)
        f.close()

        # Check if passwords found
        try:
            if(len(logins) != 0):
                info("\nSaved passwords found...")
                # Show passwords
                for i in range(len(logins)):
                    info_cont(f'{i+1}: ')
                    success(f'{logins[i][0]}\t[ {logins[i][1]} ]')
                info_cont('0: ')
                info('Someone else')
                # Enter choice
                ch = enter('Login as:(num) ')
                if(ch != '0'):
                    return logins[int(ch)-1], logins
                else:
                    return enter_login(), logins
        except:
            # error('No saved passwords')
            # Enter login details
            return enter_login(), logins
    except:
        error('Could not read file')
        return enter_login(), logins

def save_details(usn, password, logins):
    if([usn, password] not in logins):
        ch = enter('Save login details? (y/n): ')
        if(ch == 'y'):
            with open(LOGINS, 'a', encoding='utf-8') as logins_file:
                login_writer = csv.writer(logins_file)
                login_writer.writerow([usn, password])

def try_login(usn, password, driver):
    user_in = driver.find_element_by_xpath('//input[@name="j_username"]')
    user_in.send_keys(usn)
    pass_in = driver.find_element_by_xpath('//input[@name="j_password"]')
    pass_in.send_keys(password)

    login_button = driver.find_element_by_xpath('//button[@id="postloginform#/Academy/j_spring_security_check"]')
    login_button.click()

def login(driver):
    '''Logs into PESU Academy'''
    not_logged_in = True
    while(not_logged_in):
        [usn, password], logins = login_credentials()
        try_login(usn, password, driver)
        try: 
            msg = driver.find_element_by_xpath('//div[@class="login-msg"]')
            if(msg):
                error(msg.text)
        except:
            success("Logged in")
            save_details(usn, password, logins)
            not_logged_in = False

    