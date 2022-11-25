# Libraries
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_flight(source,destination,date):
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = f'https://www.kayak.es/flights/{source}-{destination}/{date}-flexible-2days?sort=bestflight_a'
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(('xpath', '//div[@class = "dDYU-close dDYU-mod-variant-default dDYU-mod-size-default"]'))).click()
    flight = driver.find_element('xpath', '//div[@class = "inner-grid keel-grid"]')

    return flight

def get_flight_details(flight):

    elementHTML = flight.get_attribute('outerHTML')
    elementSoup = BeautifulSoup(elementHTML,'html.parser')
    flight_details = []

    #date
    flight_date = elementSoup.find("span",{"class": "flag"}).get_text() #WARNING!
    flight_details.append(flight_date)

    #depart time
    depart_time = elementSoup.find("span",{"class": "depart-time base-time"}).get_text()
    flight_details.append(depart_time)

    #arrival time
    arrival_time = elementSoup.find("span",{"class": "arrival-time base-time"}).get_text()
    flight_details.append(arrival_time)

    #company names
    company_name = elementSoup.find("span",{"class": "codeshares-airline-names"}).get_text()
    flight_details.append(company_name)

    #price
    temp_price = elementSoup.find("div", {"class": "col-price result-column js-no-dtog"})
    price = temp_price.find("span", {"class": "price-text"}).get_text().strip().replace(u'\xa0', u' ') #WARNING!
    flight_details.append(price)

    return flight_details