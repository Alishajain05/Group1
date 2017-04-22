import re as re
import time
import zipcode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
from bs4 import BeautifulSoup

def find_all_zipcode(zip_items):
    #single string
    if type(zip_items) == str:
        zipcode_obj = zipcode.islike(zip_items)
        output = re.findall('\d+', str(zipcode_obj))
    elif type(zip_items) == list:
        output = [n for each in zip_items for n in re.findall('\d+', str(zipcode.islike(each)))]
    else:
        raise ValueError("input 'zip_items' must be of type str or list")
    return output

def input_grab(driver, search_term):
    output = []
    wait = WebDriverWait(driver, 10)
    # making the function deal with lists of zip codes
    if search_term is list:
        for i in range(len(search_term)):
            actions = wait.until(EC.presence_of_element_located((By.ID, "citystatezip")))
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "zsg-icon-searchglass")))
            actions.clear()
            time.sleep(3)
            actions.send_keys(search_term[1])
            time.sleep(3)
            button.click()
            time.sleep(3)
            output.append(driver.page_source)
            try:
                element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'zsg-pagination-next')))
                element.click()
                time.sleep(3)
            except TimeoutException:
                pass
            continue

    elif search_term is str:
        actions = wait.until(EC.presence_of_element_located((By.ID, "citystatezip")))
        button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "zsg-icon-searchglass")))
        actions.clear()
        time.sleep(3)
        actions.send_keys(search_term)
        time.sleep(3)
        button.click()
        time.sleep(3)

        output = []
        while True:
            # grab the data
            output.append(driver.page_source)
            # click next link
            try:
                element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'zsg-pagination-next')))
                element.click()
                time.sleep(3)
            except TimeoutException:
                break
    return output

def get_listings(list_obj):
    # Split the raw HTML into segments, one for each listing.
    output = []
    for i in list_obj:
        htmlSplit = i.split('" id="zpid_')[1:]
        output += htmlSplit
    print
    print str(len(output)) , " results scraped\n***"
    return output

zipz = find_all_zipcode('103')
url = 'https://www.zillow.com/homes/for_rent/'
driver = webdriver.Chrome()
driver.get(url)

raw_data = input_grab(driver, zipz)
listings = get_listings(raw_data)

Street_Address = []
City = []
State = []
Zip_Code = []
Price = []
SQFT = []
Bedrooms = []
Bathrooms = []
Days_on_Market = []
URL = []

for i in range(len(listings)):
    soup = BeautifulSoup(listings[i], "lxml")
    try:
        Street_Address.append(soup.find('span', {"itemprop": "streetAddress"}).get_text())
    except AttributeError:
        Street_Address.append("NA")
    try:
        City.append(soup.find('span', {"itemprop": "addressLocality"}).get_text())
    except AttributeError:
        City.append("NA")
    try:
        State.append(soup.find('span', {"itemprop": "addressRegion"}).get_text())
    except AttributeError:
        State.append("NA")
    try:
        Zip_Code.append(soup.find('span', {"itemprop": "postalCode"}).get_text())
    except AttributeError:
        Zip_Code.append("NA")
    try:
        Price.append(
            int(soup.find('span', {"class": "zsg-photo-card-price"}).get_text().split('/')[0].replace('$', '').replace(
                ',', '').replace('+','')))
    except AttributeError:
        Price.append("NA")

    try:
        # info = soup.find('span', {"class": "zsg-photo-card-info"}).get_text()
        Bedrooms.append(
            [int(s) for s in soup.find('span', {"class": "zsg-photo-card-info"}).get_text().replace(',', '').split() if
             s.isdigit()][0])
    except (ValueError, IndexError, AttributeError):
        Bedrooms.append("NA")

    try:
        Bathrooms.append(
            [int(s) for s in soup.find('span', {"class": "zsg-photo-card-info"}).get_text().replace(',', '').split() if
             s.isdigit()][1])

    except (ValueError, IndexError, AttributeError):
        Bathrooms.append("NA")

    try:
        SQFT.append(
            [int(s) for s in soup.find('span', {"class": "zsg-photo-card-info"}).get_text().replace(',', '').split() if
             s.isdigit()][2])
    except (ValueError, IndexError, AttributeError):
        SQFT.append("NA")

    try:
        Days_on_Market.append(soup.find('span', {"class": "zsg-photo-card-notification"}).get_text())
    except (ValueError, IndexError, AttributeError):
        Days_on_Market.append("NA")

columns = {'streetAddress': Street_Address, 'City': City, 'State': State, 'Zip_Code': Zip_Code,
           'Monlthly Rental': Price,
           'SQFT': SQFT, 'Bedrooms': Bedrooms, 'Bathrooms': Bathrooms, ' Days_on_Market': Days_on_Market}

# print len(Street_Address),len(City), len(State), len(Zip_Code)
# Create a dataframe from the columns variable
df = pd.DataFrame(columns)

2+2