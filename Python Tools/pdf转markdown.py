import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import markdown


def pdf_to_markdown(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all PDF files in the input folder
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        input_path = os.path.join(input_folder, pdf_file)
        output_path = os.path.join(output_folder, pdf_file.replace('.pdf', '.md'))

        with pdfplumber.open(input_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown.markdown(full_text))

        print(f"Converted {pdf_file} to {output_path}")


if __name__ == "__main__":
    input_folder = '/Users/massif/Desktop/1/'
    output_folder = '/Users/massif/Desktop/output/'
    pdf_to_markdown(input_folder, output_folder)
