from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from transformers import BlipProcessor, BlipForConditionalGeneration
from scipy.spatial import KDTree
from sklearn.metrics import silhouette_score

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
            "gray": (128, 128, 128),
            "gold": (255, 215, 0),
            "beige": (245, 245, 220),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255),
            "lime": (0, 255, 0),
            "sky blue": (135, 206, 235),
            "orange red": (255, 69, 0),
            "teal": (0, 128, 128),
            "violet": (238, 130, 238),
            "turquoise": (64, 224, 208),
            "olive": (128, 128, 0),
            "maroon": (128, 0, 0),
            "navy": (0, 0, 128),
            "aquamarine": (127, 255, 212),
            "coral": (255, 127, 80),
            "fuchsia": (255, 0, 255),
            "wheat": (245, 222, 179),
            "silver": (192, 192, 192),
            "plum": (221, 160, 221),
            "indigo": (75, 0, 130)
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
    
    def optimal_k_silhouette(self, img, max_k=8):
        silhouette_scores = []
        for n in range(3, max_k+1):  # starts from 2 clusters
            kmeans = KMeans(n_clusters=n, n_init='auto')
            kmeans.fit(img)
            score = silhouette_score(
                img, 
                kmeans.labels_,
                metric="euclidean",
                sample_size=500
            )
            print(f'n = {n}; score = {score}')
            silhouette_scores.append(score)
        optimal_k = silhouette_scores.index(max(silhouette_scores)) + 3  # +3 because index 0 corresponds to 2 clusters
        optimal_k += 1                                                   # +1 to make sure important colors are included
        print(f'optimal_k = {optimal_k}')
        return optimal_k


    def label_color(self, img):
        image = Image.open(img)
        image = image.resize((480,480))
        data = np.array(image)
        data = data.reshape(-1,3)   #reshape to (num_pixel, 3 channel)
        k = self.optimal_k_silhouette(data)

        kmeans = KMeans(n_clusters=k, n_init='auto')
        kmeans.fit(data)

        center = kmeans.cluster_centers_
        colors = center.astype(int)
        kdtree = KDTree(list(self.color_table.values()))

        color_names_list = []
        for rgb in colors:
            dist, index = kdtree.query(rgb)
            color_names_list.append(list(self.color_table.keys())[index])

        return color_names_list