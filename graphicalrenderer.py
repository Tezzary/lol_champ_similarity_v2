import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import embedding
import db
import os
import requests
from PIL import Image

embedding.load_embeddings()

#download images from datadragon
def download_champion_images():
    DATA_DRAGON_VERSION = "15.10.1"

    champions = db.get_champions()

    if not os.path.exists("champion_images"):
        os.makedirs("champion_images")

    if os.listdir("champion_images"):
        print("Champion images directory is not empty. Skipping download.")
        return
    
    for champion in champions:

        image_url = f"https://ddragon.leagueoflegends.com/cdn/{DATA_DRAGON_VERSION}/img/champion/{champion["championName"]}.png"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        img_response = requests.get(image_url, headers=headers)
        
        if img_response.status_code == 200:
            with open(f"champion_images/{champion['id']}.png", 'wb') as img_file:
                img_file.write(img_response.content)
            print(f"Downloaded {champion['id']}.png")
        else:
            print(f"Failed to download image for {champion['id']}")

def plot_tsne(embeddings_2d, filename):
    plt.figure(figsize=(10, 8))
    
    ''' 
    #Plot the t-SNE embeddings with annotations for each champion 
    labels = [champion["championName"] for champion in db.get_champions()]
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], alpha=0.5, s=10)
    for i, label in enumerate(db.get_champions()):
        plt.annotate(label["championName"], (embeddings_2d[i, 0], embeddings_2d[i, 1]), fontsize=8, alpha=0.7)
    plt.colorbar()
    '''
    #Plot the t-SNE embeddings with images for each champion
    champions = db.get_champions()

    fig, ax = plt.subplots(figsize=(12, 10))

    for champion in champions:
        try:
            img = Image.open(f"champion_images/{champion['id']}.png")
            img = img.resize((128, 128))  # Resize explicitly if needed
            imagebox = OffsetImage(img, zoom=0.125)
            x, y = embeddings_2d[champion['i'], 0], embeddings_2d[champion['i'], 1]
            ab = AnnotationBbox(imagebox, (x, y), frameon=False)
            ax.add_artist(ab)
        except Exception as e:
            print(f"Error loading {champion['id']}.png: {e}")
    ax.set_xlim(embeddings_2d[:, 0].min() - 1, embeddings_2d[:, 0].max() + 1)
    ax.set_ylim(embeddings_2d[:, 1].min() - 1, embeddings_2d[:, 1].max() + 1)
    #save to images/image.png
    plt.axis('off')  # Hide axes
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, dpi=300)

download_champion_images()

tsne = TSNE(metric='cosine', n_components=2, perplexity=30, learning_rate=200, random_state=42)
embeddings_2d = tsne.fit_transform(embedding.embeddings)
plot_tsne(embeddings_2d, 'images/image_cosine.png')

tsne = TSNE(metric='euclidean', n_components=2, perplexity=30, learning_rate=200, random_state=42)
embeddings_2d = tsne.fit_transform(embedding.embeddings)
plot_tsne(embeddings_2d, 'images/image_euclidean.png')

print("Image saved")