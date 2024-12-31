import json
import re

def create_data(ipa_file, vi_file, words_file, output_file):
    """
    Creates a data file and an error file.

    The data file contains word, IPA, and meaning information for words found in both IPA and VI files.
    The error file contains words from the words file that were not found in either the IPA or VI file.

    Args:
        ipa_file: Path to the IPA file.
        vi_file: Path to the Vietnamese meaning file.
        words_file: Path to the file containing words.
        output_file: Path to the output data file.
    """

    # Load IPA data
    ipa_data = {}
    with open(ipa_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            tab_split = line.strip().split("\t")
            if len(tab_split) != 2:
                tab_split = re.split(r'\s{1,}', line.strip(), maxsplit=1)
            
            if len(tab_split) == 2:
                word, ipa = tab_split
                ipa_data[word.lower()] = ipa
            else:
                print(f"Error at {ipa_file} at line {line_num}: Invalid format missing tab or space")

    # Load Vietnamese meaning data
    vi_data = {}
    error_lines = []
    with open(vi_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            tab_split = line.strip().split("\t")
            if len(tab_split) != 2:
                tab_split = re.split(r'\s{1,}', line.strip(), maxsplit=1)

            if len(tab_split) == 2:
                word, meaning_json = tab_split
                try:
                    vi_data[word.lower()] = json.loads(meaning_json)  # Load the meaning as JSON
                except json.JSONDecodeError as e:
                    error_lines.append(line_num)
                    print(f"Error at {word} Invalid JSON - {meaning_json} ({e})")

            else:
                print(f"Error in {vi_file} at line {line_num}: Invalid format - '{line.strip()}'")

    # Process each word and write to output file
    with open(words_file, 'r', encoding='utf-8') as f_words, \
            open(output_file, 'w', encoding='utf-8') as f_out:
        for word in f_words:
            word = word.strip().lower()
            if word in ipa_data and word in vi_data:
                meaning_str = json.dumps(vi_data[word], ensure_ascii=False)  # Convert to JSON string
                f_out.write(f"{word}\t{ipa_data[word]}\t{meaning_str}\n")
            else :
                if word not in ipa_data:
                    print(f"Word '{word}' not found in IPA file")
                if word not in vi_data:
                    print(f"Word '{word}' not found in VI file")

# Usage:
ipa_file = "ipa.txt"  # Your ipa file names
vi_file = "vi.txt"    # Your translate file names
words_file = "words.txt"    # Your words file names
output_file = "data.txt"    # Your output file names

create_data(ipa_file, vi_file, words_file, output_file)
