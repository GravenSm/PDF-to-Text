import os
import re
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path


def perform_ocr_on_single_page(pdf_path, page_num):
    images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)
    return pytesseract.image_to_string(images[0])


def perform_ocr_on_pdf(pdf_path):
    print(f"Performing OCR on: {pdf_path}")
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        texts = [perform_ocr_on_single_page(pdf_path, i) for i in range(num_pages)]
        return ' '.join(texts)


def extract_text_from_pdf(pdf_path, password=None):
    print(f"Reading PDF: {pdf_path}")
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)

        # If the PDF is encrypted, try to decrypt it with the provided password
        if reader.is_encrypted:
            if password is None:
                print(f"Password required for {pdf_path}")
                return ""
            else:
                try:
                    reader.decrypt(password)
                except Exception as e:
                    print(f"Failed to decrypt {pdf_path}: {e}")
                    return ""

        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return text


def clean_text(text):
    # Normalize whitespace by replacing any sequence of whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text)

    # Optionally, remove headers and footers
    text = re.sub(r'Header text|Footer text', '', text)

    # Remove any unwanted characters (customize the character set as needed)
    text = re.sub(r'[^a-zA-Z0-9.,;:!?()\'"-]', ' ', text)

    # Replace common OCR errors (customize based on your observation of OCR errors)
    # Example: text = text.replace('fl', 'fi')

    # Convert text to lowercase
    text = text.lower()

    # Strip leading and trailing whitespace
    text = text.strip()

    return text


def process_single_pdf(pdf_path, output_folder, root, file):
    print(f"Processing: {pdf_path}")
    text = perform_ocr_on_pdf(pdf_path)

    if len(text.strip()) == 0:
        print(f"OCR returned empty text for {pdf_path}, trying PyPDF2")
        text = extract_text_from_pdf(pdf_path)

    if len(text.strip()) == 0:
        print(f"No text extracted from {pdf_path}")
        return

    clean_text_content = clean_text(text)
    relative_path = os.path.relpath(root, input_folder)
    output_dir = os.path.join(output_folder, relative_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.txt")
    print(f"Creating text file: {output_file_path}")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(clean_text_content)
    print(f"Processed {file}")


def process_pdfs_in_directory(directory, output_folder):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                process_single_pdf(pdf_path, output_folder, root, file)


input_folder = 'SOURCE_DOCUMENTS'
output_folder = 'processed'
process_pdfs_in_directory(input_folder, output_folder)
