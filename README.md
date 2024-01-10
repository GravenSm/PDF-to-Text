# PDF-to-Text
This project involves a Python script designed to process a large collection of PDF files efficiently. 

The primary goals of the script are:
OCR Processing: It uses Optical Character Recognition (OCR) via Tesseract OCR to extract text from PDFs, especially useful for scanned documents or image-based PDFs where text extraction isn't straightforward.
Text Extraction: The script uses PyPDF2 to extract text directly for PDFs with embedded text.
Text Cleaning: After extraction, the script performs cleaning operations on the text, such as normalizing whitespace, removing unwanted characters, and converting text to lowercase to ensure consistency and readability.
Multiprocessing for Efficiency: Given the large volume of PDFs, the script employs Python's multiprocessing to parallelize the processing, significantly speeding up the task by utilizing multiple CPU cores.
Progress Tracking: It provides progress updates as it processes each file, giving visibility into the current processing state, which is especially useful for long-running operations.
The script is tailored for robustness and efficiency, making it well-suited for handling extensive collections of diverse PDF files in a scalable manner.
