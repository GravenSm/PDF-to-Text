import os
import re
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from multiprocessing import Pool, cpu_count, current_process


def perform_ocr_on_single_page(pdf_path, page_num):
    try:
        images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)
        return pytesseract.image_to_string(images[0])
    except Exception as e:
        print(f"Error in OCR processing page {page_num} of {pdf_path}: {e}")
        return ""


def perform_ocr_on_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            num_pages = len(reader.pages)
            texts = [perform_ocr_on_single_page(pdf_path, i) for i in range(num_pages)]
            return ' '.join(texts)
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return ""


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


def process_single_pdf(pdf_path, output_folder, input_folder, root, file, file_index, total_files):
    process_id = current_process().pid  # Get the process ID
    print(f"[{process_id}] Processing {file_index}/{total_files}: {pdf_path}")

    try:
        text = perform_ocr_on_pdf(pdf_path)
        if len(text.strip()) == 0:
            text = extract_text_from_pdf(pdf_path)
        if len(text.strip()) == 0:
            return
        clean_text_content = clean_text(text)
        output_dir = os.path.join(output_folder, os.path.relpath(root, input_folder))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(clean_text_content)
        print(f"[{process_id}] Finished {file_index}/{total_files}: {pdf_path}")

    except Exception as e:
        print(f"Error processing file {pdf_path}: {e}")


def process_pdfs_in_directory(input_folder, output_folder):
    all_pdf_files = [(root, file) for root, dirs, files in os.walk(input_folder) for file in files if file.endswith('.pdf')]
    total_files = len(all_pdf_files)

    pdf_files_with_progress = [(os.path.join(root, file), output_folder, input_folder, root, file, idx+1, total_files)
                               for idx, (root, file) in enumerate(all_pdf_files)]

    pool = Pool(cpu_count())
    pool.starmap(process_single_pdf, pdf_files_with_progress)
    pool.close()
    pool.join()


if __name__ == '__main__':
    input_folder = 'SOURCE_DOCUMENTS'
    output_folder = 'processed'
    process_pdfs_in_directory(input_folder, output_folder)
