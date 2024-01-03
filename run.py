from crawl import pinterest
from download_img import scrapper
from util import utility
from caption import captioning

if __name__ == "__main__":
    print("script starts!")
    util = utility()
    
    util.clean_folder('downloaded_images')
    crawler = pinterest()
    crawler.driver.get('https://www.pinterest.com/huangkaikai/ellsworth-kelly/')
    crawler.log_in()
    crawler.scroll_to_bottom()
    crawler.save_pin_urls()
    crawler.driver.close()
    
    downloader = scrapper()
    downloader.download_images()
        
    tag = 'ELLSWORTH-KELLY-ART'
    util.clean_folder('resized_images')
    util.get_dir_file_list()
    util.resize_and_crop()
    util.labeling('resized_images', tag)
    util.push_to_HF('./resized_images', tag)