import random
import math
import json

def gen_pattern_coords(pattern_type, center_x, center_y, size, num_points):
    """
    Génère une liste de coordonnées pour un pattern spécifique.

    :param pattern_type: Type de pattern ('triangle', 'square', 'x', 'rond', 'v')
    :param center_x: Coordonnée x du centre du pattern
    :param center_y: Coordonnée y du centre du pattern
    :param size: Taille du pattern
    :param num_points: Nombre de points dans le pattern
    :return: Liste de tuples (x, y) représentant les points
    """
    coords = []

    if pattern_type == 'triangle':
        for i in range(5):  # Nombre de lignes dans le triangle
            for j in range(i + 1):
                offset_x = random.randint(-1, 1)  # Décalage aléatoire
                offset_y = random.randint(-1, 1)
                px = center_x + j * size // 5 + offset_x
                py = center_y + i * size // 5 + offset_y
                coords.append((px, py))

    elif pattern_type == 'square':
        for i in range(5):
            for j in range(5):
                offset_x = random.randint(-1, 1)
                offset_y = random.randint(-1, 1)
                px = center_x + i * size // 5 + offset_x
                py = center_y + j * size // 5 + offset_y
                coords.append((px, py))

    elif pattern_type == 'x':
        for i in range(5):
            offset_x1 = random.randint(-1, 1)
            offset_y1 = random.randint(-1, 1)
            offset_x2 = random.randint(-1, 1)
            offset_y2 = random.randint(-1, 1)
            # Diagonal \
            px1 = center_x + i * size // 5 + offset_x1
            py1 = center_y + i * size // 5 + offset_y1
            coords.append((px1, py1))
            # Diagonal /
            px2 = center_x + (4 - i) * size // 5 + offset_x2
            py2 = center_y + i * size // 5 + offset_y2
            coords.append((px2, py2))

    elif pattern_type == 'rond':
        for theta in range(0, 360, 30):
            offset_x = random.randint(-1, 1)
            offset_y = random.randint(-1, 1)
            px = center_x + int(size * math.cos(math.radians(theta))) + offset_x
            py = center_y + int(size * math.sin(math.radians(theta))) + offset_y
            coords.append((px, py))
        for _ in range(num_points - len(coords)):  # Ajouter des points internes
            offset_x = random.randint(-size // 2, size // 2)
            offset_y = random.randint(-size // 2, size // 2)
            px = center_x + offset_x
            py = center_y + offset_y
            coords.append((px, py))

    elif pattern_type == 'v':
        for i in range(5):
            offset_x1 = random.randint(-1, 1)
            offset_y1 = random.randint(-1, 1)
            offset_x2 = random.randint(-1, 1)
            offset_y2 = random.randint(-1, 1)
            # Branche gauche
            px1 = center_x - i * size // 5 + offset_x1
            py1 = center_y + i * size // 5 + offset_y1
            coords.append((px1, py1))
            # Branche droite
            px2 = center_x + i * size // 5 + offset_x2
            py2 = center_y + i * size // 5 + offset_y2
            coords.append((px2, py2))

    return coords

def generate_pattern_data(width, height, num_lists, num_patterns_per_list, size):
    """
    Génère une liste de listes de patterns, chaque sous-liste contenant des patterns aléatoires.

    :param width: Largeur de l'image
    :param height: Hauteur de l'image
    :param num_lists: Nombre de listes à générer
    :param num_patterns_per_list: Nombre aléatoire maximal de patterns par liste
    :param size: Taille des patterns
    :return: Liste de listes contenant des dictionnaires (label et coordonnées)
    """
    all_data = []
    patterns = ['triangle', 'square', 'x', 'rond', 'v']

    for _ in range(num_lists):
        sublist = []
        num_patterns = random.randint(1, num_patterns_per_list)  # Nombre aléatoire de patterns
        for _ in range(num_patterns):
            pattern_type = random.choice(patterns)
            center_x = random.randint(size, width - size)
            center_y = random.randint(size, height - size)
            coords = gen_pattern_coords(pattern_type, center_x, center_y, size, 20)
            sublist.append({"label": pattern_type, "coords": coords})
        all_data.append(sublist)

    return all_data

# Génération des données
width, height, num_lists, num_patterns_per_list, size = 128, 128, 3, 5, 20
pattern_data = generate_pattern_data(width, height, num_lists, num_patterns_per_list, size)

# Sauvegarde des données dans un fichier JSON
output_file = "pattern_data.json"
with open(output_file, "w") as f:
    json.dump(pattern_data, f, indent=4)

print(f"Données sauvegardées dans {output_file}")
