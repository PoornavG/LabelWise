# Labelwise

This project is designed to extract nutritional information from an image of a nutrition label using Optical Character Recognition (OCR) via Tesseract, and then generate a detailed health report based on the extracted data using LLaMA-2, a language model from Meta.

## Features

- Extract Nutritional Data: Uses Tesseract OCR to extract nutritional information from an image of a nutrition label.
- Generate Health Report: Uses the LLaMA-2 language model to generate a detailed health report based on the extracted nutritional data, including advantages, disadvantages, and health warnings.
- Custom Image Input: Users can input the path of the image file directly in the script for convenience.
- Outputs:
- JSON-formatted nutritional data.
- A health report providing analysis and suggestions.

## Requirement

- Python 3.x
- Tesseract OCR
- Hugging Face's Transformers Library
- PyTorch

Make sure you have `bcrypt` installed. You can install it using `pip`:

```bash
pip install bcrypt
```
## Installation

Clone the repository or download the encrypt.py and verify.py files to your local machine.
```bash
git clone https://github.com/PoornavG/TwistyCrypt.git
cd TwistyCrypt
```

## Usage

### Encrypt a Password and Generate Hash

The `encrypt.py` script encrypts a password and generates a bcrypt hash using a bit-flipping algorithm.

1. Run the `encrypt.py` script:

   ```bash
   python encrypt.py
   ```
2.Enter the password when prompted:

  ```bash
      Enter the password: Hello123
  ```

## Verify a Password Against a Hash

The verify.py script verifies if the entered password matches the stored hash.

1.Run the verify.py script:

```bash
python verify.py
```

2.Enter the password and the hashed password for verification:

```bash
Enter the password for verification: Hello123
Enter the hashed password: b'$2b$12$grm.2E9oSppejVt6t92WduYu34kb6p8Rn2meTUzRbCMnouLcCAgOS'
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.

