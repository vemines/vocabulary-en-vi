import json

def create_json_from_data_file(data_file, json_file):
    """
    Creates a JSON file from a data file, ensuring the meaning field is a JSON object.

    Args:
        data_file: Path to the input data file (data.txt).
        json_file: Path to the output JSON file (data.json).
    """

    data = []
    with open(data_file, 'r', encoding='utf-8') as f_in:
        for line_num, line in enumerate(f_in, 1):
            parts = line.strip().split('\t')
            if len(parts) == 3:
                word, ipa, meaning_str = parts
                # Convert the meaning string to a JSON object
                meaning_obj = json.loads(meaning_str)

                data.append({
                    "word": word,
                    "ipa": ipa,
                    "meaning": meaning_obj
                })

            else:
                print(f"Error in {data_file} at line {line_num}: Invalid format - '{line.strip()}'")

    with open(json_file, 'w', encoding='utf-8') as f_out:
        json.dump(data, f_out, ensure_ascii=False, separators=(',', ':'))

data_file = "data.txt"
json_file = "data.json"

create_json_from_data_file(data_file, json_file)