from PIL import Image, ImageDraw
import os
import json
import numpy as np

def draw_pattern_on_image(image_size, pattern):
    """
    Dessine un pattern spécifique sur une image vierge.

    :param image_size: Taille de l'image (width, height)
    :param pattern: Dictionnaire contenant le label et les coordonnées du pattern
    :return: Image PIL avec le pattern dessiné
    """
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)

    for coord in pattern['coords']:
        x, y = coord
        draw.ellipse((x-2, y-2, x+2, y+2), fill="black")

    return image

def save_images_from_patterns(output_dir, patterns, image_size):
    """
    Sauvegarde les images générées à partir des patterns dans un répertoire.

    :param output_dir: Répertoire où sauvegarder les images
    :param patterns: Liste de dictionnaires contenant les patterns
    :param image_size: Taille de chaque image
    """
    os.makedirs(output_dir, exist_ok=True)

    for i, pattern in enumerate(patterns):
        image = draw_pattern_on_image(image_size, pattern)
        label = pattern['label']
        image_path = os.path.join(output_dir, f"pattern_{label}_{i}.png")
        image.save(image_path)
        print(f"Image sauvegardée: {image_path}")

def generate_image_array(image_size, patterns):
    """
    Génère une image à partir de plusieurs patterns et retourne l'image sous forme de tableau numpy.

    :param image_size: Taille de l'image (width, height)
    :param patterns: Liste de dictionnaires contenant les patterns
    :return: Tuple (image_array, used_patterns)
    """
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)

    used_patterns = []
    for pattern in patterns:
        used_patterns.append(pattern['label'])
        for coord in pattern['coords']:
            x, y = coord
            draw.ellipse((x-2, y-2, x+2, y+2), fill="black")

    image_array = np.array(image)
    return image_array, used_patterns

def transform_lists_to_images(data_file, output_dir, image_size=(128, 128)):
    """
    Transforme les sous-listes de patterns en images et les sauvegarde.

    :param data_file: Chemin du fichier JSON contenant les listes de patterns
    :param output_dir: Répertoire où sauvegarder les images
    :param image_size: Taille des images générées
    """
    with open(data_file, 'r') as f:
        data = json.load(f)

    all_patterns = [pattern for pattern_list in data for pattern in pattern_list]
    save_images_from_patterns(output_dir, all_patterns, image_size)

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple : Lecture des données depuis un fichier JSON généré par le premier fichier
    data_file = "pattern_data.json"  # Ce fichier doit être généré par le premier fichier
    output_directory = "output_images"
    transform_lists_to_images(data_file, output_directory)
