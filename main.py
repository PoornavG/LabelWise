import argparse
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import re
import json
from transformers import AutoTokenizer, pipeline
import torch

# Constants
VALID_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
WINDOWS_CHECK_COMMAND = 'where'
DEFAULT_CHECK_COMMAND = 'which'
TESSERACT_DATA_PATH_VAR = 'TESSDATA_PREFIX'

# Regex patterns for nutritional data extraction
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

# Tesseract helper functions
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_path(path):
    return bool(os.path.exists(path))

def get_command():
    return WINDOWS_CHECK_COMMAND if sys.platform.startswith('win') else DEFAULT_CHECK_COMMAND

def run_tesseract(filename, output_path, image_file_name):
    filename_without_extension = os.path.splitext(filename)[0]
    if not output_path:
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, filename_without_extension)
        subprocess.run(['tesseract', image_file_name, temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open(f'{temp_file}.txt', 'r', encoding="utf8") as f:
            text = f.read()
        shutil.rmtree(temp_dir)
        return text
    text_file_path = os.path.join(output_path, filename_without_extension)
    subprocess.run(['tesseract', image_file_name, text_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(f'{text_file_path}.txt', 'r', encoding="utf8") as f:
        return f.read()

def check_pre_requisites_tesseract():
    check_command = get_command()
    result = subprocess.run([check_command, 'tesseract'], stdout=subprocess.PIPE)
    if not result.stdout:
        logging.error("tesseract-ocr missing, install tesseract to resolve. Refer to README for more instructions.")
        return False
    logging.debug("Tesseract correctly installed!\n")
    return True

def clean_nutrition_data(text):
    nutrition_info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            nutrition_info[key] = match.group(1)
    return nutrition_info

# LLaMA functions for health report generation
def load_nutrition_data(nutrition_data: dict) -> dict:
    return nutrition_data

def get_llama_response(prompt: str, llama_pipeline, tokenizer) -> str:
    sequences = llama_pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=256,
    )
    return sequences[0]['generated_text']

def generate_health_report(nutrition_data: dict, llama_pipeline, tokenizer) -> None:
    prompt = f"""
    You are a health expert who generates detailed health reports based on nutritional data.
    Generate a health report based on the following nutritional data, summarize the contents, and provide suggestions or warnings in bullet points: {json.dumps(nutrition_data)}.
    """
    response = get_llama_response(prompt, llama_pipeline, tokenizer)
    print("Health Report:\n", response)

# Main function to process the image and generate JSON
def process_nutrition_data(input_path, output_path, llama_pipeline, tokenizer):
    if not check_pre_requisites_tesseract():
        return
    if not check_path(input_path):
        logging.error(f"Nothing found at {input_path}")
        return
    if output_path:
        create_directory(output_path)
        logging.debug(f"Creating Output Path {output_path}")

    if os.path.isdir(input_path):
        logging.debug("The Input Path is a directory.")
        total_file_count = len(os.listdir(input_path))
        if total_file_count == 0:
            logging.error("No files found at your input location")
            return
        other_files = 0
        successful_files = 0
        for filename in os.listdir(input_path):
            extension = os.path.splitext(filename)[1]
            if extension.lower() not in VALID_IMAGE_EXTENSIONS:
                other_files += 1
                continue
            image_file_name = os.path.join(input_path, filename)
            text = run_tesseract(filename, output_path, image_file_name)
            cleaned_data = clean_nutrition_data(text)
            if output_path:
                output_file = os.path.join(output_path, f"{os.path.splitext(filename)[0]}.json")
                with open(output_file, 'w') as json_file:
                    json.dump(cleaned_data, json_file, indent=4)
            else:
                print(json.dumps(cleaned_data, indent=4))

            # Generate health report for this file
            generate_health_report(cleaned_data, llama_pipeline, tokenizer)

            successful_files += 1
        logging.info(f"Parsing Completed! Successfully parsed images: {successful_files}, Unsupported files: {other_files}")
    else:
        filename = os.path.basename(input_path)
        text = run_tesseract(filename, output_path, input_path)
        cleaned_data = clean_nutrition_data(text)
        if output_path:
            output_file = os.path.join(output_path, f"{os.path.splitext(filename)[0]}.json")
            with open(output_file, 'w') as json_file:
                json.dump(cleaned_data, json_file, indent=4)
        else:
            print(json.dumps(cleaned_data, indent=4))

        # Generate health report for this file
        generate_health_report(cleaned_data, llama_pipeline, tokenizer)

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Single image file path or images directory path", required=True)
    parser.add_argument('-o', '--output', help="(Optional) Output directory for converted text")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable verbose DEBUG logging")

    args = parser.parse_args()
    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output) if args.output else None

    logging.getLogger().setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.debug(f"Input Path is {input_path}")

    if sys.version_info[0] < 3:
        logging.error(f"You are using Python {sys.version_info[0]}.{sys.version_info[1]}. Please use Python>=3")
        exit()

    # Initialize LLaMA pipeline
    model = "meta-llama/Llama-2-7b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=True)
    llama_pipeline = pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    # Process the data and generate health report
    process_nutrition_data(input_path, output_path, llama_pipeline, tokenizer)
