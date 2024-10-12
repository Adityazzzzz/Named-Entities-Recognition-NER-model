import re
import spacy
import pytesseract
from PIL import Image

nlp = spacy.load('en_core_web_sm')


# Path to the tesseract executable (modify the path to where you installed Tesseract)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Function to extract text from an image using OCR
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


# Function to extract named entities using SpaCy
def extract_named_entities(text):
    doc = nlp(text)
    entities = {ent.label_: ent.text for ent in doc.ents}
    return entities


# Function to extract specific information using regex
def extract_specific_info(text):

    name_pattern = r'^([A-Za-z\s]+)(?:\s\d+\.\d+%| Lotion)'
    expiry_date_pattern = r'Exp\. Date\s*:\s*(\d{2}/\d{4})'
    temperature_pattern = r'Store at temperature not exceeding (\d+ C)'
    composition_pattern = r'Composition:\s*([\w\s\.,%/]+)'
    dos_and_donts_pattern = r'Dosage:\s*([\w\s\.,:]+)|Do not [\w\s.,]+'

    name_match = re.search(name_pattern, text, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else "Name not found"#...........name

    expiry_date_match = re.search(expiry_date_pattern, text)
    expiry_date = expiry_date_match.group(1) if expiry_date_match else "Expiry date not found"#...........date

    temperature_match = re.search(temperature_pattern, text)
    temperature = temperature_match.group(1) if temperature_match else "Temperature not found"#...........temp

    composition_match = re.search(composition_pattern, text, re.DOTALL)
    composition = composition_match.group(1).strip() if composition_match else "Composition not found"#...........composition

    dos_and_donts_matches = re.findall(dos_and_donts_pattern, text, re.DOTALL)
    dos_and_donts = " ".join(match.strip() for match in dos_and_donts_matches if match.strip())#...........precautions

    return name, expiry_date, temperature, composition, dos_and_donts


# Main function to process the image and extract information
def process_image(image_path):

    text = extract_text_from_image(image_path)

    named_entities = extract_named_entities(text)
    print("Named Entities:")
    print(named_entities)

    name, expiry_date, temperature, composition, dos_and_donts = extract_specific_info(text)
    print(f"Name: {name}")
    print(f"Expiry Date: {expiry_date}")
    print(f"Temperature: {temperature}")
    print(f"Chemical Composition: {composition}")
    print(f"Dos and Don'ts: {dos_and_donts}")


# Upload Image
image_path = 'Check.jpg' 
process_image(image_path)
