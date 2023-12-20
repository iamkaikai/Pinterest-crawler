import requests
from bs4 import BeautifulSoup
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
        # options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_script_timeout(60)
        
    def scroll_to_bottom(self):
        
        time.sleep(30)
        self.get_pin_urls()
        print('save pin urls...')

        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_height = last_height / 2
            while True:
                print(f'last_height = {last_height}')
                print('-----------------')

                self.driver.execute_script(f"window.scrollTo(0, {scroll_height});")
                self.get_pin_urls()
                print('save pin urls...')
                
                time.sleep(10)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                print(f'new_height = {new_height}')            
                
                if new_height == last_height:
                    self.save_pin_urls()
                    break
                last_height = new_height
                
        except Exception as e:
            print("Error in scroll_to_bottom:", e)

    def save_pin_urls(self):
        with open('pin_ids.txt', 'a') as file:
            for pin_id in self.pin_ids_set:
                file.write(pin_id + '\n')
            
    def get_pin_urls(self):
        try:
            pins = self.driver.find_elements(By.CSS_SELECTOR, '[data-test-pin-id]')
            if pins:
                pin_ids = [self.pin_ids_set.add(pin.get_attribute('data-test-pin-id')) for pin in pins]
        except Exception as e:
            print("Error in get_pin_links:", e)


    def download_images(pin_links):
        for link in pin_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the image URL (modify selector as needed)
            image_url = soup.select_one('img.pinImage')['src']

            # Download and save the image
            img_data = requests.get(image_url).content
            with open('path/to/save/image.jpg', 'wb') as handler:
                handler.write(img_data)

    def log_in(self):
        try:
            login_btn = self.driver.find_element(By.CSS_SELECTOR, ".RCK.Hsu.USg.adn.CCY.NTm.KhY.iyn.oRi.lnZ.wsz.YbY")
            login_btn.click()
            
            email = self.driver.find_element(By.ID, 'email')
            email.send_keys(self.email)

            pwd = self.driver.find_element(By.ID, 'password')
            pwd.send_keys(self.pwd)

            submit_button = self.driver.find_element(By.CSS_SELECTOR, '[data-test-id="registerFormSubmitButton"]')
            submit_button.click()
            print('login success!')
            time.sleep(10)
        except Exception as e:
            print("Login Error: ", e)



def main():
    crawler = pinterest()
    crawler.driver.get('https://www.pinterest.com/huangkaikai/3d-microsoft/')
    crawler.log_in()
    crawler.scroll_to_bottom()
    # download_images(pin_links)
    # driver.quit()

if __name__ == "__main__":
    print('start!')
    main()
    
    
