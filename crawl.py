from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

import os


class pinterest:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv('EMAIL')
        self.pwd = os.getenv('PASSWORD')
        self.pin_ids_set = set()
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_script_timeout(60)
        self.last_height = 0

    def scroll_segments(self, height, sections):
        sub_height = (height-self.last_height) // sections
        for i in range(sections):
            print(f'scrolling section {i}...')
            self.driver.execute_script(f"window.scrollTo(0, {self.last_height + sub_height*i});")
            time.sleep(1)
            self.get_pin_urls()
        self.last_height = height
        
    def scroll_to_bottom(self):
        time.sleep(5)
        # Disable notifications - this will automatically deny notifications
        
        self.driver.maximize_window()

        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
                        
            while True:
                print(f'last_height = {last_height}')
                print('-----------------')
                self.scroll_segments(last_height, 10)                                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                print(f'new_height = {new_height}')            
                
                if new_height == last_height:
                    self.save_pin_urls()
                    break
                last_height = new_height
                
        except Exception as e:
            print("Error in scroll_to_bottom:", e)

    def save_pin_urls(self):
        with open('pin_ids.txt', 'w') as file:
            for pin_id in self.pin_ids_set:
                file.write(pin_id + '\n')
            
    def get_pin_urls(self):
        try:
            pins = self.driver.find_elements(By.CSS_SELECTOR, '[data-test-pin-id]')
            if pins:
                for pin in pins:
                    self.pin_ids_set.add(pin.get_attribute('data-test-pin-id'))
        except Exception as e:
            print("Error in get_pin_links:", e)

    def log_in(self):
        print('login...')
        try:
            login_btn = self.driver.find_element(By.CSS_SELECTOR, ".tBJ.dyH.iFc.sAJ.X8m.tg7.H2s")
            login_btn.click()
            
           
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Email"]')))  # Wait for the email field
            email = self.driver.find_element(By.CSS_SELECTOR, '[placeholder="Email"]')
            email.send_keys(self.email)
        
            pwd = self.driver.find_element(By.ID, 'password')
            pwd.send_keys(self.pwd)

            submit_button = self.driver.find_element(By.CSS_SELECTOR, '[data-test-id="registerFormSubmitButton"]')
            submit_button.click()
            print('login success!')
        except Exception as e:
            print("Login Error: ", e)

    