# Labelwise

This project is designed to extract nutritional information from an image of a nutrition label using Optical Character Recognition (OCR) via Tesseract, and then generate a detailed health report based on the extracted data using LLaMA-2, a language model from Meta.

## Features

- Extract Nutritional Data: Uses Tesseract OCR to extract nutritional information from an image of a nutrition label.
- Generate Health Report: Uses the LLaMA-2 language model to generate a detailed health report based on the extracted nutritional data, including advantages, disadvantages, and health warnings.
- Custom Image Input: Users can input the path of the image file directly in the script for convenience.
- Outputs:
- JSON-formatted nutritional data.
- A health report providing analysis and suggestions.

## Requirements

- Python 3.x
- Tesseract OCR
- Hugging Face's Transformers Library
- PyTorch

## Installation Guide(Local setup)
### Install Tesseract OCR
Linux
```bash
sudo apt update
sudo apt install tesseract-ocr
```
macOS:
```bash
brew install tesseract
```
Windows:

- Download the installer from Tesseract's official website.
- Add Tesseract to the system path.

### Install Python Dependencies

```bash
pip install pytesseract transformers torch
```
### Clone or Download the Project
```bash
git clone https://github.com/PoornavG/LabelWise
```
## Usage

#### Navigate to the project folder:
```bash
cd LabelWise
```

#### Provide Your Image
Place your image file (with a nutrition label) inside the project directory or specify its full path when running the script.

#### Run the Program

```bash
python main.py --input /path/to/your/nutrition_image.jpg
```

## Example usage
```bash
python main.py --input /path/to/your/nutrition_image.jpg --output ./output
```

