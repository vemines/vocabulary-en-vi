import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
import textwrap
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register a custom font with unicode support
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))  # Make sure you have this font file

def create_pdf_from_json_batch(batch_data, output_file, pdf_title):
    """
    Creates a PDF table from a batch of JSON data.
    
    Args:
        batch_data: A list of word objects (batch from the large JSON).
        output_file: Path to the output PDF file (data.pdf).
        pdf_title: Title of the PDF document.
    """
    # 1. Set up PDF Document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    doc.title = pdf_title

    # Margins
    margin = 0.3 * inch
    doc.leftMargin = margin
    doc.rightMargin = margin
    doc.topMargin = margin
    doc.bottomMargin = margin

    # Font and style for regular text
    font_name = 'DejaVuSans'
    font_size = 10

    normal_style = ParagraphStyle(
        'normal',
        fontName=font_name,
        fontSize=font_size,
        alignment=TA_LEFT,
        leading=font_size * 1.2  # Reduced line height
    )

    vietnamese_style = ParagraphStyle(
        'vietnamese',
        fontName=font_name,
        fontSize=font_size,
        alignment=TA_LEFT,
        leading=font_size * 1.5,
        leftIndent=0.1 * inch,
        rightIndent=0.1 * inch,
    )

    # 2. Create the Table
    col_widths = [1.2 * inch, 1.3 * inch, 1.3 * inch, 3 * inch]
    line_height = 1.2 * font_size  # Reduced line height

    table_data = []
    table_data.append(["Word", "Type", "IPA", "Vietnamese"])  # Header row

    # Type abbreviation mapping
    type_map = {
        "determiner": "det",
        "verb": "v",
        "auxiliary verb": "aux",
        "noun": "n",
        "conjunction": "conj",
        "preposition": "prep",
        "adverb": "adv",
        "adjective": "adj",
        "pronoun": "pron"
    }

    for item in batch_data:
        word = item["word"]
        ipa = item["ipa"]

        # Combine meanings from different types
        all_vietnamese_meanings = []
        types = []
        for pos, meanings in item["meaning"].items():
            types.append(type_map.get(pos, pos))
            all_vietnamese_meanings.extend(meanings)

        type_str = ", ".join(types)
        vietnamese_str = "; ".join(all_vietnamese_meanings)

        table_data.append([word, type_str, ipa, vietnamese_str])

    table_elements = []

    for row_index, row in enumerate(table_data):
        row_elements = []
        row_heights = []

        for col_index, text in enumerate(row):
            if col_index == 3:
                p = Paragraph(text, vietnamese_style)
            else:
                p = Paragraph(text, normal_style)

            row_elements.append(p)

            # Calculate cell height
            if col_index == 3:
                wrapped_text = textwrap.wrap(text, width=45)  # Adjust width as needed
                num_lines = len(wrapped_text)
                cell_height = max(num_lines, 1) * line_height
            else:
                cell_height = line_height
                # Reduce cell height for "Type" column
                if col_index == 1 and row_index != 0 :
                    cell_height = line_height * 0.5

            row_heights.append(cell_height)

        max_height = max(row_heights)

        # Adjust alignment and leading for cells
        new_row = []
        for col_index, p in enumerate(row_elements):
            if col_index != 3:
                p.style.alignment = TA_CENTER

                # Vertically center the first 3 columns
                if max_height > p.style.leading:
                    p.style.leading = max_height - (max_height - p.style.leading) / 2
                else:
                    p.style.leading = max_height

                # Further reduce leading for "Type" column
                if col_index == 1 and row_index != 0:
                    p.style.leading = line_height * 0.5

                new_row.append(p)
            else:
                new_row.append(p)

        table_elements.append(new_row)

    table = Table(table_elements, colWidths=col_widths)
    table.setStyle(TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), font_name),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically center all cells
    ]))

    # 4. Build and Save the PDF
    story = [table]
    doc.build(story)

def split_and_process_json(input_json_file, batch_size=5000):
    """
    Split the large JSON into smaller chunks and process them to generate PDFs.
    
    Args:
        input_json_file: Path to the large input JSON file.
        batch_size: Number of words per batch (default 5000).
    """
    # Read the large JSON file
    with open(input_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Split the data into smaller chunks
    num_batches = len(data) // batch_size + (1 if len(data) % batch_size != 0 else 0)

    # Process each batch and create PDFs with appropriate naming
    for i in range(num_batches):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, len(data))  # Ensure we don't go beyond the data length
        
        batch_data = data[start_index:end_index]
        
        # Generate the PDF filename based on the chunk range with cleaner names
        start_str = f"{start_index // 1000}k"
        end_str = f"{end_index // 1000}k"
        output_pdf = f"data_{start_str}-{end_str}.pdf"
        
        # Call the PDF creation function
        create_pdf_from_json_batch(batch_data, output_pdf, pdf_title="Common English Words with Meanings")
        print(f"PDF generated for range {start_str}-{end_str}: {output_pdf}")

# Usage
input_json_file = 'dictionary/data/data.json'  # Path to the large input JSON file
split_and_process_json(input_json_file, batch_size=5000)
