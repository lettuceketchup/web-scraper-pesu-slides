import requests
import csv
from time import sleep
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
# Wait for loading
def wait_for(driver, path, time = 10):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, path))
    )
    return element

# Connect to database
def connect(driver):
    '''Connect to PESU Academy'''
    try:
        task("\nConnecting to PESU Academy...")
        driver.get(URL)
        success("Connected")
        try:
            task('Page Loading...')
            wait_for(driver, '//button[@id="postloginform#/Academy/j_spring_security_check"]')
            success('Page Loaded')
        except:
            error('Page not loaded')
    except:
        error("Could not connect to PESU Academy")
        exit_program(driver)


# Authentication Functions
def enter_login():
    '''Enter login details'''
    task('\nEnter login details')
    usn = enter('USN: ')
    password  = enter('Password: ')
    return usn, password

def login_credentials(default):
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
                if(default == -1):
                    ch = enter('Login as:(num) ')
                else:
                    sleep(0.5)
                    ch = default
                    # task('Default choice: ' + default)
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

def login(driver, default = -1):
    '''Logs into PESU Academy'''
    not_logged_in = True
    while(not_logged_in):
        [usn, password], logins = login_credentials(default)
        try_login(usn, password, driver)
        try: 
            msg = driver.find_element_by_xpath('//div[@class="login-msg"]')
            if(msg):
                error(msg.text)
        except:
            success("Logged in")
            save_details(usn, password, logins)
            not_logged_in = False

# Subject List
def get_subject_list(driver):
    wait_for(driver, "//span[contains(text(), 'My Courses')]//..//..//a").click()
    table = wait_for(driver, '//table')
    table_rows = table.find_elements_by_xpath(".//tr")[1::]
    return table_rows

def chose_subject(driver, subject_list):
    i = 1
    task('\nSubjects-')
    for row in subject_list:
        sb_row = row.find_elements_by_xpath(".//td")[0:2]
        task(i, end=' ')
        info_cont(sb_row[0].text + '\t')
        info(sb_row[1].text)
        i+=1

    while(True):
        ch = int(enter("Choose Subject: ")) - 1
        if(ch >= 0 and ch < len(subject_list)):
            subject_list[ch].click()
            return
        else:
            error('Enter a valid choice')

def chose_category():
    print()
    info("1: AV Summary")
    info('2: Live Videos')
    info('3: Slides')
    info('0: All three!')
    return enter('Choose category: ')

def choose_units(driver):
    list = wait_for(driver, "//ul[@id='courselistunit']")
    unit_list = list.find_elements_by_xpath(".//*//a")
    task("\nUnits-")
    for i in range(len(unit_list)):
        task(i+1, end= ': ')
        info(unit_list[i].text)
    task(0, end= ': ')
    info('All units')
    unit = int(enter('Choose unit: '))
    if(unit == 0):
        return unit_list
    elif(unit > 0 and unit <= len(unit_list)):
        return [unit_list[unit-1]]

    