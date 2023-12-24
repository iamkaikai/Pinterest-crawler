import requests
from bs4 import BeautifulSoup
import os

class scrapper:
    def __init__(self):
        pass
    
    def get_img_from_pin_url(self, url):
        if url.isdigit() and len(url) == 18:
            url = f'https://www.pinterest.com/pin/{url}'
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                img_elements = soup.find_all('img')
                first_img_element = img_elements[0]
                image_url = first_img_element['src'] if 'src' in first_img_element.attrs else None
                return image_url
            else:
                print(f"Failed to retrieve the webpage: Status code {response.status_code}")
                return None

    def download_images(self):
        if not os.path.exists('downloaded_images'):
            os.makedirs('downloaded_images')
            
        with open('pin_ids.txt', 'r') as file:
            for line in file:
                pin_id = line.strip()
                image_url = self.get_img_from_pin_url(pin_id)
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        file_path = os.path.join('downloaded_images', f'image_{pin_id}.jpg')
                        with open(file_path, 'wb') as img_file:
                            img_file.write(response.content)
                        print(f"Downloaded {pin_id} as {file_path}")
                    else:
                        print(f"Failed to download image: Status code {response.status_code}")
                except Exception as e:
                    print(f"Error downloading image: {e}")
