import time
import allure

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from base.base_class import Base


class Main_page(Base):

    url = 'https://effective-mobile.ru/'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    select_about = "a.tn-atom[href='#about']"
    select_info = "a.tn-atom[href='#moreinfo']"
    select_cases = "a.tn-atom[href='#cases']"
    select_reviews = "a.tn-atom[href='#Reviews']"
    select_contacts = "a.tn-atom[href='#contacts']"

    # Getters
    def get_about(self):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.select_about)))

    def get_info(self):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.select_info)))

    def get_cases(self):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.select_cases)))

    def get_reviews(self):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.select_reviews)))

    def get_contacts(self):
        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.select_contacts)))

    # Actions

    def click_select_about(self):
        el = self.get_about()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)
        print("Click select about")

    def click_select_info(self):
        el = self.get_info()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)
        print("Click select info")

    def click_select_cases(self):
        el = self.get_cases()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)
        print("Click select cases")

    def click_select_reviews(self):
        el = self.get_reviews()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)
        print("Click select reviews")

    def click_select_contacts(self):
        el = self.get_contacts()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)
        print("Click select contacts")

    # Methods

    def select_main_page(self):
        with allure.step("Select main page"):
            self.driver.get(self.url)
            self.driver.maximize_window()
            time.sleep(2)
            WebDriverWait(self.driver, 15).until(lambda d: d.execute_script("return document.readyState") == "complete")
            self.get_current_url()
            self.click_select_about()
            self.assert_url('https://effective-mobile.ru/#about')
            time.sleep(2)
            self.click_select_info()
            self.assert_url('https://effective-mobile.ru/#moreinfo')
            time.sleep(2)
            self.click_select_cases()
            self.assert_url('https://effective-mobile.ru/#cases')
            time.sleep(2)
            self.click_select_reviews()
            self.assert_url('https://effective-mobile.ru/#Reviews')
            time.sleep(2)
            self.click_select_contacts()
            self.assert_url('https://effective-mobile.ru/#contacts')
