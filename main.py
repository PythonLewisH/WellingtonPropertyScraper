import time

import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Google form that will be filled in with browser automation
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSceSHCYn-MAmEU-3jEG5M64IwBTvwPJObfWJmJxPhf3udkNlg/viewform" \
              "?usp=sf_link"

# Website where code will be scraping data from
REALESTATE_URL = "https://www.realestate.co.nz/residential/rental/wellington"


# Headers for my browser
headers = {'Accept-Language': 'en-US,en;q=0.9',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/100.0.4896.127 Safari/537.36 '
           }

# Retrieves data from website
response = requests.get(REALESTATE_URL, headers=headers)

# Creates a python object from the website hmtl. "lxml" parser used but needed to be installed.
soup = BeautifulSoup(response.content, "lxml")

# Finds all the prices of properties on the webpage with the specific class
prices = soup.find_all(class_='text-gray-750 font-bold leading-tight flex justify-start text-xl.25 mb-3.5 lg:mb-2 '
                              'xl:mb-3.5')

# Properties near the bottom of the page had slightly different class so saving these in another variable
prices2 = soup.find_all(class_='text-gray-750 font-bold leading-tight flex justify-start text-xl.25 mb-3.5 xl:mb-5 '
                               'text-sm xl:text-base')

# Below joins together all of the prices found into a list.
all_prices = []
for i in range(len(prices)):
    all_prices.append(prices[i].text.replace(" \xa0per week", ""))

for i in range(len(prices2)):
    all_prices.append(prices2[i].text.replace(" \xa0per week", ""))


# Finds all the links to the properties on the page and saves into a list
all_link_elements = soup.select(".tile--body a")
all_links = []
for i in range(len(all_link_elements)):
    all_links.append(all_link_elements[i]["href"])


# Finds all the addresses of the properties on the page and saves into a list
all_addresses = []
listing_details = soup.find_all(class_="pr-3 text-sm.5 xl:text-lg text-navy-500 font-bold leading-tight tracking-tight capitalize mb-1")
for i in range(len(listing_details)):
    all_addresses.append(listing_details[i].text.replace("\n    ", ""))

listing_details2 = soup.find_all(class_="pr-3 text-sm.5 xl:text-lg text-navy-500 font-bold leading-tight tracking-tight capitalize mb-3")
for i in range(len(listing_details2)):
    all_addresses.append(listing_details2[i].text.replace("\n", ""))

# Prints to check code working correctly and for easier debugging
print(all_addresses)
print(all_prices)
print(all_links)

# Initialises Chrome Web Driver (will need a different driver for safari, firefox etc...)
service = Service("/Users/LewisHudson/Desktop/Development/chromedriver")
driver = webdriver.Chrome(service=service)


# Defines a function for using selenium to input the address, price and link into the google form. Sleep is initiated
# to allow time for browser to load properly.
def fill_forms(address, price, link):
    driver.get(GOOGLE_FORM)
    time.sleep(5)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                                  '1]/div/div[1]/input')
    address_input.send_keys(address)
    time.sleep(2)
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                                '1]/div/div[1]/input')
    price_input.send_keys(price)
    time.sleep(2)
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                               '1]/div/div[1]/input')
    link_input.send_keys("https://www.realestate.co.nz/residential/rental/wellington" + link)
    time.sleep(2)
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()
    time.sleep(2)


# For loop that inputs each item in the address, price and link lists into the function.
for i in range(len(all_addresses)):
    fill_forms(all_addresses[i], all_prices[i], all_links[i])






