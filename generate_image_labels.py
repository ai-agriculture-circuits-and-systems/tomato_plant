import json
import os
import time
import random

# Paths
# These are now relative to the project root
DATA_JSON_PATH = os.path.join('data', 'data.json')
IMAGES_DIR = os.path.join('data', 'images')

# Load data.json
with open(DATA_JSON_PATH, 'r') as f:
    data = json.load(f)

info = data['info']
categories = data['categories']
annotations = data['annotations']
images = data['images']

# Helper to generate unique 10-digit id
def generate_unique_id():
    base = random.randint(1000000, 9999999)  # 7 digits
    timestamp = int(time.time() * 1000) % 1000  # last 3 digits from ms timestamp
    return int(f"{base}{timestamp:03d}")

# Group annotations by image_id
annotations_by_image = {}
for ann in annotations:
    img_id = ann['image_id']
    if img_id not in annotations_by_image:
        annotations_by_image[img_id] = []
    # Copy annotation and replace id
    ann_copy = ann.copy()
    ann_copy['id'] = generate_unique_id()
    annotations_by_image[img_id].append(ann_copy)

# Process each image
for img in images:
    img_id = img['id']
    img_filename = img['file_name']
    img_json_name = os.path.splitext(img_filename)[0] + '.json'
    img_json_path = os.path.join(IMAGES_DIR, img_json_name)

    # Build JSON structure
    output = {
        'info': info,
        'images': [img],
        'annotations': annotations_by_image.get(img_id, []),
        'categories': categories
    }

    # Save JSON
    with open(img_json_path, 'w') as f:
        json.dump(output, f, indent=2)

print("All image label JSON files have been generated.") 