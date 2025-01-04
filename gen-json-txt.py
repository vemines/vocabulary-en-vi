import json

def create_json_from_data_file(data_file, json_file, word_count=5000):
    """
    Creates a JSON file from a data file, ensuring the meaning field is a JSON object,
    includes parts, and adds an incrementing ID. Allows specifying a maximum word count.

    Args:
        data_file: Path to the input data file (data.txt).
        json_file: Path to the output JSON file (data.json).
        word_count: The maximum number of words to process (default is 5000).
    """

    data = []
    id_counter = 1
    with open(data_file, 'r', encoding='utf-8') as f_in:
        for line_num, line in enumerate(f_in, 1):
            if id_counter > word_count:
                break  # Stop if word_count is reached

            parts = line.strip().split('\t')
            if len(parts) == 4:
                word, ipa, parts_str, meaning_str = parts
                # Convert the meaning string and parts string to a JSON object
                meaning_obj = json.loads(meaning_str)
                parts_obj = json.loads(parts_str)

                data.append({
                    "id": id_counter,
                    "word": word,
                    "ipa": ipa,
                    "parts": parts_obj,
                    "meaning": meaning_obj
                })
                id_counter += 1

            else:
                print(f"Error in {data_file} at line {line_num}: Invalid format - '{line.strip()}'")

    with open(json_file, 'w', encoding='utf-8') as f_out:
        json.dump(data, f_out, ensure_ascii=False, separators=(',', ':'))

data_file = "dictionary/data/data.txt"
json_file = "dictionary/data/data_10k.json"
word_count = 53966   # 53966

create_json_from_data_file(data_file, json_file, word_count)