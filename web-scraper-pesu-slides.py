import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, deinit
from colors import task, success, error, info, info_cont

# Define constants/paths
DRIVER_PATH = './chromedriver'
URL = 'https://pesuacademy.com/'
DOWNLOAD_PATH = './Sounds/'

# Initialize colorama
init()

# Functions

def get_sound(name, page):
    '''Search wikipedia page for sound file and downlaod it'''
    try:
        try:
            source = page.find_element_by_xpath("//table[@class='infobox']//tbody//tr[last()]//td//div[2]//small//a[1]")
            print(source.get_attribute('href'))
            source.click()
            downloadUrl = page.find_element_by_xpath("//div[@class='fullMedia']//p//a").get_attribute('href')
        except:
            return error("Download link not found on Wikipedia")
        print(downloadUrl)
        r = requests.get(downloadUrl, allow_redirects=True)
        open(DOWNLOAD_PATH + name + '.ogg', 'wb').write(r.content)
        return success("Downloaded")
    except:
        return error("Not Downloaded")
    

def get_page(i, phoneme, name, link):
    '''Open phoneme link in new window and search for wikilink'''
    page = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    page.get(link)
    try:
        wikiLink = page.find_element_by_xpath("//h2[1]//a")
        info(name)
        wikiLink.click()
        status = get_sound(name, page)
        return status
    except:
        info(name)
        return error("WikiLink not found on Phoible")
    finally:
        page.quit()


def search_in_database(i, phoneme):
    '''Search phoneme on phoible'''
    search.clear()
    search.send_keys(phoneme)
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//tbody//tr//a[@title="' + phoneme + '"]'))
        )
        name = element.find_element_by_xpath("..//..//td[3]").text
        status = get_page(i, phoneme, name, element.get_attribute('href'))
        return status, name
    except:
        return error("Not found on Phoible")

# Function to exit program
def exit_program():
    '''Exit selenium_python program'''
    # Quit chromedriver
    driver.quit()

    # De-initialize colorama
    deinit()

# Gather phonemes
phonemes = []
with open('indian_union.txt', encoding='UTF-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        phonemes = row
task(phonemes)
print()

# Initialize chromedriver
task("Initializing...")
options = Options()
options.headless = True
options.add_argument('--log-level=3')
options.add_argument("--window-size=1920,1200")

try:
    task("\nStarting Browser...")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    success("Started")
except:
    error("Could not start Browser")
    exit_program()

# Connect to database
try:
    task("Connecting to Phoible...")
    driver.get(URL)
    success("Connected")
except:
    error("Could not connect to Phoible")
    exit_program()

# Look for search input
try:
    task("Looking for search input...")
    search = driver.find_element_by_id('dt-filter-name')
    success("Searchbox found")
except:
    error("Searchbox not found")
    exit_program()


'''Start search'''
# Open status_file
status_file = open('union.csv', 'a', newline='', encoding='UTF-16')
status_writer = csv.writer(status_file)


# for i in range(188, 192):
for i in range(len(phonemes)):
    status = search_in_database(i+1, phonemes[i])
    status_writer.writerow([phonemes[i], status[0], status[1]])

# Close status_file
status_file.close()

exit_program()