import os
from PyPDF2 import PdfMerger

def merge_pdfs(pdf_files, output_filename="merged_output.pdf"):
    """
    Merges specified PDF files into a single PDF in the given order.

    Args:
        pdf_files: A list of PDF file paths in the desired order.
        output_filename: The name of the output merged PDF file.
    """
    merger = PdfMerger()

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    merger.write(output_filename)
    merger.close()
    print(f"Merged PDF created: {output_filename}")

# Define the desired order of PDF files
pdf_order = [
    "data_0k-5k.pdf",
    "data_5k-10k.pdf",
    "data_10k-15k.pdf",
    "data_15k-20k.pdf",
    "data_20k-25k.pdf",
    "data_25k-30k.pdf",
    "data_30k-35k.pdf",
    "data_35k-40k.pdf",
    "data_40k-45k.pdf",
    "data_45k-50k.pdf",
    "data_50k-53k.pdf",
]

pdf_folder = "."  # Change this if your PDFs are in a different folder
pdf_files = [os.path.join(pdf_folder, f) for f in pdf_order]

# Check if all files exist
for file_path in pdf_files:
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        exit()
        
# Merge the PDFs in the specified order
merge_pdfs(pdf_files, output_filename="data.pdf")