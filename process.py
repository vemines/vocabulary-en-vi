import google.generativeai as genai
import asyncio
import argparse
import os

genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key

# prompt_type == 
#   "translate" for translate task, 
#   "ipa" for IPA task
def get_promt(prompt_type, text):
    # Define both prompt templates
    if prompt_type == "translate":
       return f"""
Translate the following English words into Vietnamese, providing ALL common meanings for EACH part of speech.

Format: English Word<tab>{"part_of_speech_1": ["meaning 1", "meaning 2", ...], "part_of_speech_2": ["meaning 1", "meaning 2", ...], ...}

<tab> is a literal tab. No extra spaces. The right side of the tab must be a valid JSON string. Be accurate, complete, and concise.

Input:
{text}
"""
    elif prompt_type == "ipa":
        return f"""
   Provide the International Phonetic Alphabet (IPA) transcriptions for the following English words, 
    using General American English pronunciation.

    For each word, use this format:

    "English Word"<tab>"/IPA Transcription/

    <tab> is a literal tab. No extra spaces. Be accurate, complete, and concise.
    - Enclose the IPA transcription within forward slashes (/).
    - Be accurate and use standard IPA symbols.
    - If a word has multiple possible pronunciations, provide the most common one.

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
        response = await model.generate_content_async(get_promt("ipa", text))
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