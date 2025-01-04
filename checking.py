import re

def preprocess_text(text):
    """Lowercase and removes non-alphanumeric characters"""
    text = text.lower()
    text = re.sub(r'[^a-z ]', '', text)
    return text

# Read the words from words.txt into a set for fast lookup
try:
    with open('dictionary/words.txt', 'r', encoding="utf-8") as words_file:
        words = {preprocess_text(line.strip()) for line in words_file}
except FileNotFoundError:
    print("Error: 'dictionary/words.txt' not found. Please check the path.")
    exit()

# Read the content of vi.txt
try:
    with open('vi.txt', 'r', encoding="utf-8") as checking_file:
        checking_content = preprocess_text(checking_file.read())
except FileNotFoundError:
    print("Error: 'vi.txt' not found. Please check the path.")
    exit()

# Check each word from words.txt to see if it exists in vi.txt
for word in words:
    if word and word not in checking_content: #added check if word is not empty
        print(f"'{word}' not found")
