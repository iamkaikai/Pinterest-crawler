from PIL import Image
import os
import csv
from datasets import load_dataset

class utility:
    def __init__(self):
        self.file_list = []
        
    
    def get_dir_file_list(self, dir='downloaded_images'):
        if not os.path.exists(dir):
            print(f"Directory '{dir}' does not exist.")
            return []
        self.file_list = [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]
        
    def resize_and_crop(self, size=(512, 512)):
        if not os.path.exists('resized_images'):
                os.makedirs('resized_images')
        
        count = 0
        
        for file in self.file_list:
            if file == '.DS_Store':
                continue
            
            image_path = os.path.join('downloaded_images', file)
            pin_id = file.split('_')[1].split('.')[0]
            
            with Image.open(image_path) as img:
                target_ratio  = size[0] / size[1]
                img_ratio = img.width / img.height
                
            
                if img_ratio == target_ratio:
                    img = img.resize(size, Image.ANTIALIAS)
                else:
                    if img_ratio > target_ratio:
                        # Image is wider than desired ratio
                        new_height = size[1]
                        new_width = int(new_height * img_ratio)
                    else:
                        # Image is taller than desired ratio
                        new_width = size[0]
                        new_height = int(new_width / img_ratio)

                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    
                    left = (new_width - size[0]) / 2
                    top = (new_height - size[1]) / 2
                    right = (new_width + size[0]) / 2
                    bottom = (new_height + size[1]) / 2
                    img = img.crop((left, top, right, bottom))
                    
                file_path = os.path.join('resized_images', f'image_{pin_id}_{size[0]}_{size[1]}.jpg')
                img.save(file_path)
                print(f'saving {file_path}...')

    def labeling(self, dir, text):
        csv_file = f'./{dir}/metadata.csv'
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['file_name', 'text'])
            
            for filename in os.listdir(dir):
                if filename in ['.DS_Store','metadata.csv']:
                    continue
                writer.writerow([filename, text])
                
    def push_to_HF(self, directory = './resized_images', repo_name=None):
        
        # Get a list of all files in the directory
        files_in_directory = os.listdir(directory)

        # Iterate over the files
        for file in files_in_directory:
            if file == '.DS_Store':
                continue
            
            file_path = os.path.join(directory, file)
            try:
                with Image.open(file_path) as img:
                    # Convert the image to RGB mode
                    print(img.info)
                    rgb_img = img.convert('RGB')
                    rgb_img.save(file_path)
            except Exception as e:
                print(f"Error for file {file}: {e}")

        # Now you can load the dataset
        print('-------')
        dataset = load_dataset("imagefolder", data_dir=directory)
        dataset.push_to_hub(f"iamkaikai/{repo_name}")
        print('Pushed to HF!')


