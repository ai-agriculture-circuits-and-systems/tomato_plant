import os
import json
from PIL import Image
import glob
import argparse
from tqdm import tqdm
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_image_label_pair(img_path, label_path):
    """Validate that image and label files exist and are readable."""
    if not os.path.exists(img_path):
        logger.warning(f"Image file not found: {img_path}")
        return False
    if not os.path.exists(label_path):
        logger.warning(f"Label file not found: {label_path}")
        return False
    try:
        Image.open(img_path)
        with open(label_path, 'r') as f:
            f.read()
        return True
    except Exception as e:
        logger.error(f"Error reading files {img_path} or {label_path}: {str(e)}")
        return False

def convert_to_coco(images_dir, labels_dir, output_file):
    """
    Convert YOLO format annotations to COCO format for the Tomato Plant dataset.
    
    Args:
        images_dir (str): Directory containing the image files
        labels_dir (str): Directory containing the YOLO format label files
        output_file (str): Path to save the COCO format JSON file
    """
    # Initialize COCO format
    coco_format = {
        "info": {
            "description": "Tomato Plant Dataset - Images of tomato plants with bounding box annotations",
            "version": "1.0",
            "year": 2024,
            "contributor": "Tomato Plant Research",
            "date_created": datetime.now().strftime("%Y/%m/%d"),
            "url": ""
        },
        "licenses": [
            {
                "id": 1,
                "name": "CC BY 4.0",
                "url": "https://creativecommons.org/licenses/by/4.0/"
            }
        ],
        "images": [],
        "annotations": [],
        "categories": [
            {
                "id": 0,
                "name": "tomato_plant",
                "supercategory": "plant"
            },
            {
                "id": 1,
                "name": "tomato_fruit",
                "supercategory": "fruit"
            }
        ]
    }
    
    # Get all image files (support both .jpg and .JPG)
    image_files = sorted(glob.glob(os.path.join(images_dir, "*.jpg"))) + \
                 sorted(glob.glob(os.path.join(images_dir, "*.JPG")))
    
    if not image_files:
        raise ValueError(f"No image files found in {images_dir}")
    
    logger.info(f"Found {len(image_files)} images in {images_dir}")
    
    # Statistics
    stats = {
        "total_images": len(image_files),
        "processed_images": 0,
        "skipped_images": 0,
        "total_annotations": 0,
        "class_counts": {0: 0, 1: 0}
    }
    
    annotation_id = 1
    
    # Process each image with progress bar
    for img_path in tqdm(image_files, desc="Converting annotations"):
        try:
            # Get image info
            img = Image.open(img_path)
            width, height = img.size
            
            # Get corresponding label file
            img_filename = os.path.basename(img_path)
            label_filename = os.path.splitext(img_filename)[0] + ".txt"
            label_path = os.path.join(labels_dir, label_filename)
            
            # Validate image-label pair
            if not validate_image_label_pair(img_path, label_path):
                stats["skipped_images"] += 1
                continue
            
            # Add image info to COCO format
            coco_format["images"].append({
                "id": len(coco_format["images"]) + 1,
                "license": 1,
                "file_name": img_filename,
                "height": height,
                "width": width,
                "date_captured": datetime.now().strftime("%Y-%m-%d")
            })
            
            # Read and convert annotations
            with open(label_path, 'r') as f:
                for line in f:
                    try:
                        class_id, x_center, y_center, w, h = map(float, line.strip().split())
                        
                        # Validate coordinates
                        if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                            logger.warning(f"Invalid coordinates in {label_path}: {line.strip()}")
                            continue
                        
                        # Convert YOLO format to COCO format (x, y, width, height)
                        x = (x_center - w/2) * width
                        y = (y_center - h/2) * height
                        w = w * width
                        h = h * height
                        
                        # Add annotation to COCO format
                        coco_format["annotations"].append({
                            "id": annotation_id,
                            "image_id": len(coco_format["images"]),
                            "category_id": int(class_id),
                            "bbox": [x, y, w, h],
                            "area": w * h,
                            "segmentation": [],
                            "iscrowd": 0
                        })
                        
                        # Update statistics
                        stats["class_counts"][int(class_id)] += 1
                        stats["total_annotations"] += 1
                        annotation_id += 1
                        
                    except ValueError as e:
                        logger.error(f"Error parsing line in {label_path}: {line.strip()}. Error: {e}")
            
            stats["processed_images"] += 1
            
        except Exception as e:
            logger.error(f"Error processing {img_path}: {str(e)}")
            stats["skipped_images"] += 1
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(coco_format, f, indent=2)
    
    # Log statistics
    logger.info("\nConversion Statistics:")
    logger.info(f"Total images found: {stats['total_images']}")
    logger.info(f"Successfully processed: {stats['processed_images']}")
    logger.info(f"Skipped images: {stats['skipped_images']}")
    logger.info(f"Total annotations: {stats['total_annotations']}")
    logger.info("Annotations by class:")
    for class_id, count in stats["class_counts"].items():
        class_name = next(cat["name"] for cat in coco_format["categories"] if cat["id"] == class_id)
        logger.info(f"  {class_name}: {count}")
    
    logger.info(f"\nCOCO format JSON saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert YOLO format annotations to COCO format for the Tomato Plant dataset')
    parser.add_argument('--images', type=str, default="data/images", help='Directory containing the image files')
    parser.add_argument('--labels', type=str, default="data/labels", help='Directory containing the YOLO format label files')
    parser.add_argument('--output', type=str, default="data/data.json", help='Path to save the COCO format JSON file')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    convert_to_coco(args.images, args.labels, args.output)