import google.generativeai as genai
import asyncio
import argparse
import os

genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key

# prompt_type == 
#   "translate" for translate task, 
#   "ipa" for IPA task
#   "parts" for IPA task
def get_promt(prompt_type, text):
    # Define both prompt templates
    if prompt_type == "translate":
       return f"""
You are a helpful translation bot. A user will provide an English word. You need to translate that word into Vietnamese, identify its common English parts of speech, and provide a list of the most relevant meanings for each part of speech in Vietnamese.

The output should be formatted as follows:

`<word>\t{{"<pos1>": ["<meaning1>", "<meaning2>", ...], "<pos2>": ["<meaning3>", ...], ...}}`

Where:
- `<word>` is the input English word.
- `\\t` represents a tab character.
- The output after \t is a JSON object.
- `<pos1>`, `<pos2>`, etc., are the English parts of speech (e.g., "noun", "verb").
- The values for each part of speech are lists of the most common and relevant Vietnamese meanings of the word when used as that part of speech.

Focus on providing the most common and direct translations, similar to how Google Translate presents its top results. Avoid less common or overly nuanced meanings unless they are very frequently encountered.

Input:
{text}
"""
    elif prompt_type == "ipa":
        return f"""
   Provide the International Phonetic Alphabet (IPA) transcriptions for the following English words, 
    using General American English pronunciation.

    For each word, use this format:

    "English Word"<tab>/IPA Transcription/

    <tab> is a literal tab. No extra spaces. Be accurate, complete, and concise.
    - Enclose the IPA transcription within forward slashes (/).
    - Be accurate and use standard IPA symbols.
    - If a word has multiple possible pronunciations, provide the most common one.

    Input:
    {text}
    """
    elif prompt_type == "parts":
        return f"""
You are an expert in English phonetics. Your task is to split each English word in the input into parts based on its pronunciation according to the American phonetics standard. Mark the primary stress within each part using a prime symbol (') placed *before* the stressed syllable.

For each word, use this format:
Format: English Word<tab>["part1", "part2", ...]

* <tab>: Represents a *literal tab character*.
* part is split based on syllables and stress. For example, the word "example" is split into ["ex", "'am", "ple"]. word part only, not ipa transcriptions.
* Be accurate, complete and concise.

Your response should be based on the accurate American phonetic pronunciation of the input words. only word parts with the stress (') symbol.

Input:
{text}
    """

async def generate_data(text, input_file):
    """Translates a block of text using the Gemini Pro model."""
    model = genai.GenerativeModel(
        "gemini-2.0-flash-exp",
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            top_k=1, 
            top_p=1,
        ),
    )
    
    try:
        response = await model.generate_content_async(get_promt("translate", text))
        return response.text
    except Exception as e:
        print(f"Error process {input_file}: {e}")
        return ""

async def main(input_file, output_file):
    """Reads text from input file, process it, and writes the result to a output file."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    response_text = await generate_data(text, input_file)

    if response_text:
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(response_text)
        print(f"Process {input_file} completed.")
        file_path = os.path.join("./", input_file)
        os.remove(file_path)

# Set up argument parser
parser = argparse.ArgumentParser(description="Translate text from one file and save to another.")
parser.add_argument("input_file", help="Input file to read text from")
parser.add_argument("output_file", help="Output file to save translated text")

# Parse arguments
args = parser.parse_args()

# Run the translation asynchronously
asyncio.run(main(args.input_file, args.output_file))