from bs4 import BeautifulSoup

import re

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.common.exceptions import NoSuchElementException

from http_api import search_stop, search_operator

class _Expedition():
    def __init__(self, date, html=None, origin=None, destination=None, departure=None, arrival=None, on_demand=None, operator=None, line=None):
        if html != None and date != None:
            self._set_parameters_from_html(html, date)

        elif origin != None and destination != None and departure != None and arrival != None and on_demand != None and date != None:
            self.origin = origin
            self.destination = destination
            self.departure = datetime.strptime(f"{departure}-{date.strftime('%d/%m/%Y')}", "%H:%M-%d/%m/%Y")
            self.arrival = datetime.strptime(f"{arrival}-{date.strftime('%d/%m/%Y')}", "%H:%M-%d/%m/%Y")
            self.on_demand = on_demand
            self.operator = operator
            self.line = line

        else:
            raise Exception("It is needed to specify the 'date' and either the 'html' argument or all the rest of them")

    def _set_parameters_from_html(self, html, date):
        data = html.find_all('td')
        self.on_demand = bool(re.search("Servizo baixo demanda", str(data[0])))
        self.origin = data[3].get_text()
        self.departure = datetime.strptime(f"{data[4].get_text()}-{date.strftime('%d/%m/%Y')}", "%H:%M-%d/%m/%Y")
        self.destination = data[5].get_text()
        self.arrival = datetime.strptime(f"{data[6].get_text()}-{date.strftime('%d/%m/%Y')}", "%H:%M-%d/%m/%Y")
        self.line = data[7].find('strong').text
        self.operator = " ".join(str(data[7]).split("\n")[3].split("<br>")[0].split()) #Super advanced AI to get the operator name Xd

    def get_origin_object(self):
        self.origin_obj = search_stop(self.origin)[0]
        return self.origin_obj
    
    def get_destination_object(self):
        self.destination_obj = search_stop(self.destination)[0]
        return self.destination_obj

    def get_operator_object(self):
        self.operator_obj = search_operator(self.operator)[0]
        return self.operator_obj

    def turn_strings_into_objects(self):
        return self.get_origin_object(), self.get_destination_object(), self.get_operator_object()


class Trip():
    def __init__(self, origin, destination, date):
        self.origin = origin
        self.destination = destination
        self.date = date

        driver = webdriver.Firefox()
        wait = WebDriverWait(driver, 10)

        driver.get("https://www.bus.gal/gl")

        #Set origin stop
        driver.find_element(By.NAME, "ori").send_keys(origin.name)
        wait.until(visibility_of_element_located((By.ID, "ui-id-1"))) #Waits until the stop selector is visible and so it can press enter
        driver.find_element(By.NAME, "ori").send_keys(Keys.RETURN)

        #Set destination stop
        driver.find_element(By.NAME, "des").send_keys(destination.name)
        wait.until(visibility_of_element_located((By.ID, "ui-id-2"))) #Waits until the stop selector is visible and so it can press enter
        driver.find_element(By.NAME, "des").send_keys(Keys.RETURN)

        #Set the date of the trip
        driver.find_element(By.NAME, "date[date]").send_keys(date.strftime("%d/%m/%Y"))
        driver.find_element(By.NAME, "date[date]").send_keys(Keys.RETURN)

        driver.find_element(By.XPATH, '//button[normalize-space()="Buscar"]').click()
        
        self.expeditions = []
        page=1
        while True: #It repeats until it fails loading the next page number
            def _check_if_page_changed_succesfully(driver): #Checks if the expected page number button is active this confirms the correct page is loaded and that it has done it correctly
                return 'active' in driver.find_element(By.XPATH, f'//button[normalize-space()="{str(page)}"]').get_attribute('class')
            wait.until(_check_if_page_changed_succesfully)
            html = driver.page_source
            soup_data = BeautifulSoup(html, features="lxml")
            expeditions_data = soup_data.find_all('tr')
            expeditions_html = expeditions_data[2:int((len(expeditions_data)-2)/5+2)] #Find all <tr> tags and remove all of them which aren't expeditions (2 first ones aren't and there 5 times the number of real expeditions of redundant <tr>)
            for expedition in expeditions_html:
                self.expeditions.append(_Expedition(date=date, html=expedition))
            try:
                page+=1
                driver.find_element(By.XPATH, f'//button[normalize-space()="{str(page)}"]').click()
            except NoSuchElementException:
                break