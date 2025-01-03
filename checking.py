# Read the words from words.txt into a set for fast lookup
with open('words.txt', 'r', encoding="utf-8") as words_file:
    words = {line.strip() for line in words_file}

# Read the content of .txt
with open('parts.txt', 'r', encoding="utf-8") as abc_file:
    abc_content = abc_file.read().lower()

# Check each word from words.txt to see if it exists in abc.txt
for word in words:
    if word not in abc_content:
        print(f'{word} not found')
