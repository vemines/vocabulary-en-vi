def split_file(filepath, start_line, end_line, lines_per_file):
    """Splits a file into multiple parts based on specified parameters.

    Args:
      filepath: The path to the input file.
      start_line: The starting line number (1-based index).
      end_line: The ending line number (1-based index).
      lines_per_file: The number of lines to include in each output file.
    """

    try:
        with open(filepath, 'r', encoding="utf-8") as f:
            lines = f.readlines()

        # Adjust line numbers to 0-based indexing
        start_line -= 1
        end_line -= 1

        if end_line >= len(lines):
            end_line = len(lines)

        # Validate input parameters
        if start_line < 0 or start_line > end_line:
            print("Error: Invalid start_line or end_line.")
            return

        if lines_per_file <= 0:
            print("Error: lines_per_file must be greater than 0.")
            return

        # Extract the relevant portion of the file
        relevant_lines = lines[start_line: end_line + 1]

        # Split into parts and write to files
        file_count = 1
        for i in range(0, len(relevant_lines), lines_per_file):
            part_lines = relevant_lines[i: i + lines_per_file]
            output_filename = f"part_{file_count}.txt"
            with open(output_filename, 'w', encoding="utf-8") as outfile:
                outfile.writelines(part_lines)
            file_count += 1

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")

# Usage
filepath = "words.txt"
start_line = 1
end_line = 5000
lines_per_file = 5000

split_file(filepath, start_line, end_line, lines_per_file)