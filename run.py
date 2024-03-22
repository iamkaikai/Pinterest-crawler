from crawl import pinterest
from download_img import scrapper
from util import utility
from caption import captioning

boards = [
    ('https://www.pinterest.com/huangkaikai/matisse/','MATISSEE-ART'),
    ('https://www.pinterest.com/huangkaikai/photo-illustration/','PHOTO-ILLUSTRATION-ART'),
    ('https://www.pinterest.com/huangkaikai/impressionism/','IMPRESSIONISM-ART'),
    ('https://www.pinterest.com/huangkaikai/basquiat/','BASQUIAT-ART'),
    ('https://www.pinterest.com/huangkaikai/bauhaus/','BAUHAUS-ART'),
    ('https://www.pinterest.com/huangkaikai/plexus/','FUI-ART'),
    ('https://www.pinterest.com/huangkaikai/baroque/','BAROQUE'),
    ('https://www.pinterest.com/huangkaikai/op-art/','OPTICAL-ART'),
    ('https://www.pinterest.com/huangkaikai/cubism/','CUBISM-ART'),
]

if __name__ == "__main__":
    util = utility()
    for board_address, tag in boards:
        print(f"Start scrapping from {board_address}!!!")
        util.clean_folder(f'downloaded_images/{tag}')
        crawler = pinterest()
        crawler.driver.get(board_address)
        crawler.log_in()
        crawler.scroll_to_bottom()
        crawler.save_pin_urls()
        crawler.driver.close()
        
        downloader = scrapper(tag)
        downloader.download_images()
            
        # util.clean_folder('resized_images')
        # util.get_dir_file_list()
        # util.resize_and_crop()
        # util.labeling('resized_images', tag)
        # util.push_to_HF('./resized_images', tag)