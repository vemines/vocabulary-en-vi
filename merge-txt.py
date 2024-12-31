import os
import re

folder_path = './'  # Replace with your folder path
output_file_path = 'output.txt'  # Output file name

# List all .txt files in the folder
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt') and f != 'words.txt']

# Sort files based on the numerical part of the filename (e.g., _part_1.txt, _part_2.txt, ...)
txt_files.sort(key=lambda x: int(re.search(r'(\d+)', x).group()))

# Open the output file for writing
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Iterate over each sorted text file in the folder
    for txt_file in txt_files:
        txt_file_path = os.path.join(folder_path, txt_file)
        
        # Open the current text file and read its lines
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Remove leading/trailing whitespaces and skip empty lines
                if line.strip():
                    output_file.write(line)

        # Delete the file after merging, excluding 'words.txt'
        os.remove(txt_file_path)

print(f'Files merged. Output saved to {output_file_path}')
