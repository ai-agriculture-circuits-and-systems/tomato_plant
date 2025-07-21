# Tomato Plant Factory Dataset

A comprehensive dataset of tomato images captured in a plant factory environment, designed for object detection and classification tasks. The dataset features micro tomato variety images with annotations for both green and red fruits.

## Dataset Description

The Tomato Plant Factory Dataset contains high-resolution images of micro tomatoes captured in an artificial light plant factory environment. This dataset is specifically designed for computer vision and deep learning applications in agricultural detection and classification tasks.

- **Number of classes**: 2 (Green and Red tomatoes)
- **Total images**: 520
- **Total instances**: 9,112
  - Green fruits: 5,996 instances
  - Red fruits: 3,116 instances
- **Image resolutions**: 
  - 6000x4000
  - 4032x3024
- **Annotation formats**: PascalVOC, YOLO, and custom JSON

## Dataset Structure

The dataset is organized as follows:
- `data/images/`: Contains all high-resolution tomato plant images.
- `data/data.json`: The main metadata file, containing all image information, annotation details, and category definitions.
- `data/images/*.json`: For each image, a corresponding JSON label file is generated, containing only the annotations relevant to that image.

### Database Structure (`data/data.json`)

The `data.json` file is a single JSON object with the following keys:
- **info**: General information about the dataset (description, version, year, contributor, source, license).
- **images**: A list of image objects, each with:
  - `id`: Unique image identifier
  - `width`, `height`: Image dimensions
  - `file_name`: Image file name
  - `size`: File size in bytes
  - `format`: Image format (e.g., JPEG)
  - `url`, `hash`, `status`: Additional metadata
- **annotations**: A list of annotation objects, each with:
  - `id`: Unique annotation identifier
  - `image_id`: The ID of the image this annotation belongs to
  - `category_id`: The category label for the annotation
  - `segmentation`: Segmentation data (if available)
  - `area`: Area of the bounding box
  - `bbox`: Bounding box coordinates `[x, y, width, height]`
- **categories**: A list of category objects, each with:
  - `id`: Unique category identifier
  - `name`: Category name (e.g., AppleBBCH76)
  - `supercategory`: Higher-level grouping

### JSON Label Format (`data/images/*.json`)

For each image, a JSON label file is generated in the same directory, named after the image (e.g., `DSC_1046_17kv10r3k_0.json`). Each label file contains:
- **info**: Copied from `data.json`
- **images**: A list with a single image object (the current image)
- **annotations**: All annotation objects from `data.json` that reference this image, with unique 10-digit IDs (last 3 digits include a timestamp for uniqueness)
- **categories**: Copied from `data.json`

This structure ensures that each image has a self-contained annotation file, making it easy to use for training and evaluation in object detection and classification tasks.

## Applications

This dataset can be used for:
- Tomato fruit detection
- Fruit maturity classification
- Yield estimation
- Harvesting robot development
- Intelligent control systems
- Plant factory automation
- Computer vision research
- Deep learning model training

## Categories

- Computer Science
- Artificial Intelligence
- Computer Vision
- Object Detection
- Machine Learning
- Agriculture
- Deep Learning
- Plant Factory
- Precision Agriculture

## Citation

If you use this dataset in your research, please cite:

Wu, Zhenwei; Wang, Xinfa; Liu, Minghao; Sun, Chengxiu (2023), "Tomato Plant Factory Dataset", Mendeley Data, V1, doi: 10.17632/8h3s6jkyff.1

## License

This dataset is licensed under CC BY 4.0 and is publicly available for research purposes.

## Source

The dataset is available at:
- [Mendeley Data](https://data.mendeley.com/datasets/8h3s6jkyff/1)
- [Papers with Code](https://paperswithcode.com/dataset/tomato-detection) 