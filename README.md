This script can handle complex directory structures, process each PDF file found within these structures, and then output the results in an organized manner that mirrors the original folder layout. This approach ensures that the output is easy to navigate and directly corresponds to the input file locations. 
Here's how it accomplishes this:

Directory Traversal: The script uses Python's os.walk() function to recursively traverse the directory tree starting from a specified root folder (input_folder). This function navigates through each directory and subdirectory, finding all PDF files.

PDF Processing: For each PDF file found, the script performs one of two actions:
  OCR Processing: If the PDF is image-based or the text extraction yields little to no text, it uses OCR (via Tesseract OCR) to extract text from the images in the PDF.
  Text Extraction: For PDFs with readable text, it uses PyPDF2 to extract text directly from the PDF.

Text Cleaning: After extracting text from a PDF, the script cleans the text by normalizing whitespace, removing unwanted characters, and converting it to lowercase.

Maintaining Directory Structure in Output:
  The script determines its relative path from the input_folder for each PDF file processed.
  It then replicates this relative path in the output_folder. This means if a PDF is located in [input_folder]/subfolder1/subfolder2/file.pdf, the corresponding output text file will be located in [output_folder]/subfolder1/subfolder2/file.txt.
  This structure is maintained by creating corresponding subdirectories in the output_folder as needed.

Multiprocessing for Efficiency: The script utilizes Python's multiprocessing to process multiple PDFs in parallel, significantly speeding up the processing time. This is especially useful when dealing with many files across various folders.

Progress Indication: As the script processes each file, it prints out messages indicating which file is being processed and its progress, offering transparency and tracking capability during the operation.
