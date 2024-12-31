import json
import openpyxl
from openpyxl.styles import Font, Alignment

def create_excel_from_json(json_file, excel_file):
    """
    Creates an Excel file (.xlsx) from a JSON data file with specified formatting.

    Args:
        json_file: Path to the input JSON file (data.json).
        excel_file: Path to the output Excel file (data.xlsx).
    """
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

    # Create a new Excel workbook and add a sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Words"

    # Write the header row
    header = ["Word", "Types", "IPA", "Vietnamese"]
    ws.append(header)

    # Apply font size 14, bold and center alignment to the header row
    for cell in ws[1]:  # ws[1] represents the first row (header)
        cell.font = Font(size=12, bold=True)  # Set font size to 14 and bold
        cell.alignment = Alignment(horizontal='center', vertical='center')  # Center alignment

    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f_json:
        data = json.load(f_json)

        # Fill in the data rows
        for item in data:
            word = item["word"]
            ipa = item["ipa"]

            # Combine meanings from different types
            all_vietnamese_meanings = []
            types = []
            for pos, meanings in item["meaning"].items():
                types.append(type_map.get(pos, pos))
                all_vietnamese_meanings.extend(meanings)

            # Create the type string (e.g., "n, v, adj")
            type_str = ", ".join(types)
            # Create the Vietnamese meanings string (e.g., "cái; con; người")
            vietnamese_str = "; ".join(all_vietnamese_meanings)

            # Write the data row
            ws.append([word, type_str, ipa, vietnamese_str])

    # Save the Excel file
    wb.save(excel_file)

# Example usage
json_file = "data.json"
excel_file = "data.xlsx"

create_excel_from_json(json_file, excel_file)
