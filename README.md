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
- Hugging Face API Access (for accessing the LLaMA-2 model)

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
#### Setup Hugging Face Authentication
###### Hugging Face API Key
To access the LLaMA-2 model via Hugging Face, you need an API key.

- Sign up or log in to your Hugging Face account at https://huggingface.co/.
- Navigate to your API token page.
- Create a new token (if you don't already have one) and copy the token.

###### Authenticate Hugging Face Locally
You need to log in to the Hugging Face API from your local environment. Run the following command in your terminal:
```bash
huggingface-cli login
```
Paste your API token when prompted.
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
## Google Colab Setup

If you prefer to use Google Colab, here’s how you can do it:

### Open Google Colab
You can use the provided Colab notebook for easy setup. Open Google Colab and create a new notebook.

### Install Dependencies in Colab
In a Colab notebook, run the following commands to install necessary dependencies:
```bash
!sudo apt install tesseract-ocr
!pip install pytesseract transformers torch
```
### Setup Hugging Face Authentication
###### Hugging Face API Key
To access the LLaMA-2 model via Hugging Face, you need an API key.

- Sign up or log in to your Hugging Face account at https://huggingface.co/.
- Navigate to your API token page.
- Create a new token (if you don't already have one) and copy the token.

###### Authenticate Hugging Face Locally
You need to log in to the Hugging Face API from your local environment. Run the following command in your terminal:
```bash
huggingface-cli login
```
Paste your API token when prompted.
### Upload Your Image
Upload your nutrition label image to the Colab environment
```bash
from google.colab import files
uploaded = files.upload()
image_file_path = list(uploaded.keys())[0]  # Select the first uploaded file
```
### Run the Code
Copy and paste the project code into the Colab notebook. Set the image_file_path to the uploaded file:
```bash
image_file_path = "/content/your_uploaded_image.jpg"  # Adjust this to your file name
```
- Then, run the script to extract nutritional data and generate the health report.
