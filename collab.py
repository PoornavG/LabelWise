# Step 1: Install dependencies (Tesseract and transformers)
!sudo apt install tesseract-ocr
!pip install pytesseract transformers torch

import os
import json
import re
import subprocess
import logging
import pytesseract
from transformers import AutoTokenizer, pipeline
import torch

# Constants
VALID_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

# Define the regex patterns for extracting nutritional information
patterns = {
    "Serving Size": r"Per\s*([\d\s\w\(\)\/]+)",
    "Calories": r"Calories\s*(\d+)",
    "Total Fat": r"Fat\s*(\d+\.?\d*)\s*g",
    "Saturated Fat": r"Saturated\s*(\d+\.?\d*)\s*g",
    "Trans Fat": r"Trans\s*(\d+\.?\d*)\s*g",
    "Cholesterol": r"Cholesterol\s*(\d+)\s*mg",
    "Sodium": r"Sodium\s*(\d+)\s*mg",
    "Total Carbohydrate": r"Carbohydrate\s*(\d+)\s*g",
    "Dietary Fiber": r"Fiber\s*(\d+)\s*g",
    "Sugars": r"Sugars\s*(\d+)\s*g",
    "Protein": r"Protein\s*(\d+)\s*g",
    "Vitamin D": r"Vitamin D\s*(\d+\.?\d*)\s*ug",
    "Calcium": r"Calcium\s*(\d+)\s*mg",
    "Iron": r"Iron\s*(\d+\.?\d*)\s*mg",
    "Potassium": r"Potassium\s*(\d+)\s*mg",
    "Vitamin A": r"Vitamin A\s*(\d+\.?\d*)\s*ug",
    "Vitamin C": r"Vitamin C\s*(\d+\.?\d*)\s*mg"
}

# Function to check if Tesseract is installed
def check_pre_requisites_tesseract():
    result = subprocess.run(['which', 'tesseract'], stdout=subprocess.PIPE)
    if not result.stdout:
        logging.error("Tesseract OCR missing. Install tesseract to continue.")
        return False
    logging.debug("Tesseract is installed!\n")
    return True

# Function to clean the nutritional data extracted by Tesseract
def clean_nutrition_data(text):
    nutrition_info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            nutrition_info[key] = match.group(1)
    return nutrition_info

# Function to run Tesseract and extract text from the image
def run_tesseract(image_file):
    text = pytesseract.image_to_string(image_file)
    return text

# Function to process the nutrition data from images
def process_nutrition_data(image_file_path):
    if not check_pre_requisites_tesseract():
        return None
    if not os.path.exists(image_file_path):
        logging.error(f"File not found at {image_file_path}")
        return None
    
    logging.debug("Processing the image file.")
    text = run_tesseract(image_file_path)
    cleaned_data = clean_nutrition_data(text)
    return cleaned_data

# Function to load the LLaMA model
def load_llama_model():
    model = "meta-llama/Llama-2-7b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=True)
    llama_pipeline = pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    return llama_pipeline, tokenizer

# Function to generate a health report using LLaMA
def generate_health_report(nutrition_data, llama_pipeline, tokenizer):
    prompt = f"""
    You are a health expert who generates detailed health reports based on nutritional data.
    Generate a health report based on the following nutritional data, summarize the contents and tell in detail the advantages or disadvantages of certain components present in the food: {json.dumps(nutrition_data)}.
    Provide suggestions or warnings in bullet points based on the data.
    """

    # Get the LLaMA model response
    sequences = llama_pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=256,
    )
    
    # Print the response (health report)
    print("Health Report:\n", sequences[0]['generated_text'])

# Main function to process images and generate the health report
def main(image_file_path):
    # Step 1: Extract nutritional data from image using Tesseract
    nutrition_data = process_nutrition_data(image_file_path)
    if nutrition_data:
        print("Nutritional Data Extracted:\n", json.dumps(nutrition_data, indent=4))
        
        # Step 2: Load LLaMA model
        llama_pipeline, tokenizer = load_llama_model()

        # Step 3: Generate health report based on the extracted nutritional data
        generate_health_report(nutrition_data, llama_pipeline, tokenizer)

# --- EXAMPLE USAGE ---
if __name__ == "__main__":
    # Specify your image file path here in "/path/to/your/image" format
    image_file_path = "/content/your_image.jpg"  # Change this to your image path

    # Run the main function
    main(image_file_path)
