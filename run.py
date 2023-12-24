from crawl import pinterest
from download_img import scrapper
from util import utility

if __name__ == "__main__":
    print("start!")
    crawler = pinterest()
    crawler.driver.get('https://www.pinterest.com/huangkaikai/3d-microsoft/')
    crawler.log_in()
    crawler.scroll_to_bottom()
    crawler.save_pin_urls()
    
    downloader = scrapper()
    downloader.download_images()
    
    util = utility()
    util.get_dir_file_list()
    util.resize_and_crop()
    util.labeling('resized_images','FluentUI')
    util.push_to_HF('./resized_images', 'FluentUI')
    