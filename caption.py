from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from transformers import BlipProcessor, BlipForConditionalGeneration
from scipy.spatial import KDTree

class captioning:
    def __init__(self, mode=True, model="Salesforce/blip-image-captioning-large"):
        self.GPU = mode
        self.processor = BlipProcessor.from_pretrained(model)
        self.color_table = {
            "red": (255, 0, 0),
            "green": (0, 128, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "orange": (255, 165, 0),
            "purple": (128, 0, 128),
            "pink": (255, 192, 203),
            "brown": (165, 42, 42),
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "light gray": (128, 128, 128),
            "gray": (50,50,50),
            "gold": (255, 215, 0),
            "beige": (245, 245, 220),
            "cyan": (0, 255, 255),
            "purple": (128, 0, 128),
            "magenta": (255, 0, 255),
            "lime": (0, 255, 0),
            "sky blue": (135, 206, 235),
            "orange red": (255, 69, 0),
            "teal": (0, 128, 128),
            "violet": (238, 130, 238),
            "turquoise": (64,224,208)
        }
    
    def label_content(self, img, prompt=None):
        img_url = img 
        raw_image = Image.open(img_url).convert('RGB')
        text = prompt

        if self.GPU:
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")
            if text:
                inputs = self.processor(raw_image, text, return_tensors="pt").to("cuda")
            else:
                inputs = self.processor(raw_image, return_tensors="pt").to("cuda")
        else:
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
            if text:
                inputs = self.processor(raw_image, text, return_tensors="pt")
            else:
                inputs = self.processor(raw_image, return_tensors="pt")

        out = model.generate(**inputs, max_new_tokens=500)
        return self.processor.decode(out[0], skip_special_tokens=True)

    def label_color(self, img, k=5):
        image = Image.open(img)
        image = image.resize((360,360))
        data = np.array(image)
        data = data.reshape(-1,3)   #reshape to (num_pixel, 3 channel)

        kmeans = KMeans(n_clusters=k, n_init=20)
        kmeans.fit(data)

        center = kmeans.cluster_centers_
        colors = center.astype(int)
        kdtree = KDTree(list(self.color_table.values()))

        color_names_list = []
        for rgb in colors:
            dist, index = kdtree.query(rgb)
            color_names_list.append(list(self.color_table.keys())[index])

        return color_names_list