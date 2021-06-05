from bs4 import BeautifulSoup

import re

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.common.exceptions import NoSuchElementException

from .http_api import search_stop, search_operator

class _Expedition():
    """
    Represents any of the expeditions of a Trip. Get's it's own data from html code

    :param html: <tr> tag for the expedition
    :type html: BeautifulSoup

    :param date: Date the expeditions take place. Just the day matters
    :type date: datetime.datetime
    """

    def __init__(self, html, date):   
        data = html.find_all('td')

        self.on_demand = bool(re.search("Servizo baixo demanda", str(data[0])))
        """
        Whether th stop is on demand 

        :type: bool
        """

        self.origin = data[3].get_text()
        """
        Origin stop name

        :type: str
        """

        self.departure = datetime.strptime(f"{data[4].get_text()}-{date.strftime('%d/%m/%Y')}", "%H:%M-%d/%m/%Y")
        """
        Deaparture time

        :type: datetime.datetime
        """

        self.destination = data[5].get_text()
        """
        Destination stop name

        :type: str
        """

        self.arrival = datetime.strptime(f"{data[6].get_text()}-{date.strftime('%d/%m/%Y')}", "%H:%M-%d/%m/%Y")
        """
        Arrival time

        :type: datetime.datetime
        """

        self.line = data[7].find('strong').text
        """
        Bus line

        :type: str
        """

        self.operator = " ".join(str(data[7]).split("\n")[3].split("<br>")[0].split()) #Super advanced AI to get the operator name Xd
        """
        Operator name

        :type: str
        """

        self.url = f"https://www.bus.gal{data[8].find('a')['href']}"
        """
        Url on bus.gal for the expedition page

        :type: str
        """

    def get_origin_object(self):
        """
        Turns the origin attribute into an object

        :return: Origin stop object
        :rtype: _Stop
        """
        
        self.origin_obj = search_stop(self.origin)[0]

        return self.origin_obj
    
    def get_destination_object(self):
        """
        Turns the destination attribute into an object

        :return: Destination stop object
        :rtype: _Stop
        """
        
        self.destination_obj = search_stop(self.destination)[0]
        return self.destination_obj

    def get_operator_object(self):
        """
        Turns the operator attribute into an object

        :return: Operator object
        :rtype: _Operator
        """

        self.operator_obj = search_operator(self.operator)[0]
        return self.operator_obj

    def turn_strings_into_objects(self):
        """
        Executes and returns the values of get_origin_object(), get_destination_object() and get_operator_object(). In that order

        :return: Operator object
        :rtype: list[_Stop, _Stop, _Operator]
        """

        return self.get_origin_object(), self.get_destination_object(), self.get_operator_object()


class Trip():
    """
    Trip class. Used for getting results as Expedition objects
    
    :param origin: Origin stop
    :type origin: _Stop

    :param destination: Destination stop
    :type destination: _Stop

    :param date: The date the trip will take place. Just the day matters
    :type date: datetime.datetime
    """

    def __init__(self, origin, destination, date):
        self.origin = origin
        """
        Origin stop

        :type: _Stop
        """

        self.destination = destination
        """
        Destination stop

        :type: _Stop
        """
        self.date = date

        self.expeditions = self._set_expeditions_from_web()
        """
        List of avaliable expeditions

        :type: list[_Expedition]
        """

        
    def _set_expeditions_from_web(self):
        """
        Obtains all the expeditions from the bus.gal web. Uses Selenium. Called on creation

        :return: List of avaliable expeditions
        :rtype: list[_Expedition]
        """
        
        driver = webdriver.Firefox()
        wait = WebDriverWait(driver, 10)

        driver.get("https://www.bus.gal/gl")

        #Set origin stop
        driver.find_element(By.NAME, "ori").send_keys(self.origin.name)
        wait.until(visibility_of_element_located((By.ID, "ui-id-1"))) #Waits until the stop selector is visible and so it can press enter
        driver.find_element(By.NAME, "ori").send_keys(Keys.RETURN)

        #Set destination stop
        driver.find_element(By.NAME, "des").send_keys(self.destination.name)
        wait.until(visibility_of_element_located((By.ID, "ui-id-2"))) #Waits until the stop selector is visible and so it can press enter
        driver.find_element(By.NAME, "des").send_keys(Keys.RETURN)

        #Set the date of the trip
        driver.find_element(By.NAME, "date[date]").send_keys(self.date.strftime("%d/%m/%Y"))
        driver.find_element(By.NAME, "date[date]").send_keys(Keys.RETURN)

        driver.find_element(By.XPATH, '//button[normalize-space()="Buscar"]').click()
        
        self.expeditions = []
        page=1
        while True: #It repeats until it fails loading the next page number
            def _check_if_page_changed_succesfully(driver): #Checks if the expected page number button is active this confirms the correct page is loaded and that it has done it correctly
                if page == 1:
                    try:
                        driver.find_element(By.XPATH, f'//strong[normalize-space()="{self.date.strftime("%d/%m/%Y")}"]')
                        return True
                    except NoSuchElementException:
                        try:
                            driver.find_element(By.XPATH, '//div[normalize-space()="Non se atoparon resultados cos criterios de búsqueda seleccionados."]') #Checks if there weren't results
                            return True
                        except NoSuchElementException:
                            return False

                return 'active' in driver.find_element(By.XPATH, f'//button[normalize-space()="{str(page)}"]').get_attribute('class')
            wait.until(_check_if_page_changed_succesfully)
            try:
                driver.find_element(By.XPATH, '//div[normalize-space()="Non se atoparon resultados cos criterios de búsqueda seleccionados."]') #Checks if there weren't results
                self.expeditions = None
                break
            except NoSuchElementException:
                pass
            html = driver.page_source
            soup_data = BeautifulSoup(html, features="lxml")
            expeditions_data = soup_data.find_all('tr')
            expeditions_html = expeditions_data[2:int((len(expeditions_data)-2)/5+2)] #Find all <tr> tags and remove all of them which aren't expeditions (2 first ones aren't and there 5 times the number of real expeditions of redundant <tr>)
            for expedition in expeditions_html:
                self.expeditions.append(_Expedition(date=self.date, html=expedition))
            try:
                page+=1
                driver.find_element(By.XPATH, f'//button[normalize-space()="{str(page)}"]').click()
            except NoSuchElementException:
                break

        driver.quit()

        return self.expeditions
