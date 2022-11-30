# Libraries
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Getting flight details from Kayak.es with the BeautifulSoup library
def get_flight_details(source,destination,date):
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = f'https://www.kayak.es/flights/{source}-{destination}/{date}-flexible-2days?sort=bestflight_a'
    driver.get(url)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(('xpath', '//div[@class = "dDYU-close dDYU-mod-variant-default dDYU-mod-size-default"]'))).click()
    try:
        flight = driver.find_element('xpath', '//div[@class = "inner-grid keel-grid"]')
    except:
        flight = driver.find_element('xpath', '//ol[@class = "resultInner"]')

    elementHTML = flight.get_attribute('outerHTML')
    elementSoup = BeautifulSoup(elementHTML,'html.parser')
    flight_details = []

    # Getting date
    try:
        flight_date = elementSoup.find("span",{"class": "flag"}).get_text()
    except:
        try:
            flight_date = elementSoup.find("div",{"class": "bottom"}).get_text()
        except:
            flight_date = "Unknown date"
    flight_details.append(flight_date)

    # Appending source
    flight_details.append(source)

    # Getting depart time
    try:
        depart_time = elementSoup.find("span",{"class": "depart-time base-time"}).get_text()
    except:
        depart_time = "Unknown depart time"
    flight_details.append(depart_time)

    # Appending destination
    flight_details.append(destination)

    # Getting arrival time
    try:
        arrival_time = elementSoup.find("span",{"class": "arrival-time base-time"}).get_text()
    except:
        arrival_time = "Unknown arrival time"
    flight_details.append(arrival_time)

    # Getting company names (airlines)
    try:
        company_name = elementSoup.find("span",{"class": "codeshares-airline-names"}).get_text()
    except Exception as e:
        print(e)
        company_name = "Unknown airline"
    flight_details.append(company_name)

    # Getting price
    try:
        temp_price = elementSoup.find("div", {"class": "col-price result-column js-no-dtog"})
        price = temp_price.find("span", {"class": "price-text"}).get_text().strip().replace(u'\xa0', u'')
    except Exception as e:
        print(e)
        price = "Unknown price"
    flight_details.append(price)

    return flight_details