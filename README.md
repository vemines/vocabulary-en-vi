# Vocabulary-en-vi

[DOWNLOAD DATA](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fvemines%2Fvocabulary-en-vi%2Ftree%2Fmain%2Fdictionary%2Fdata)

## Description

This project uses the Gemini Ai model to translate list of words. It includes functionality to generate International Phonetic Alphabet (IPA) transcriptions, part of word for learning and translate it to Vietnamese.

## Features

- IPA transcriptions for English words.
- Translate word to vietnamese.
- Word part base on pronounce
- Generate raw TXT file.
- Generate JSON from TXT. Compact json.
- Generate XLSX from JSON.
- Generate PDF from JSON.
- Update later ...

## Install

1. Clone the repository:
   ```sh
   git clone https://github.com/vemines/vocabulary-en-vi.git
   ```
2. Navigate to the project directory:
   ```sh
   cd vocabulary-en-vi
   ```
3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Python

#### [split-line.py](split-line.py): chunk your list file seperate by line. modify filepath, start_line, end_line, lines_per_file base on you purpose.

#### [merge-txt.py](merge-txt.py): merge all .txt exclude "words.txt" and "requirements.txt" to one file.

#### [checking.py](checking.py): checking words from 2 file. is word from "words.txt" exist in ex: "parts.txt"

#### [process.py](process.py) input_flie output_file: Load input_file, put text to promt (modify promt type at `response = await model.generate_content_async(get_promt("translate", text))`). "ipa" for generate ipa file. "translate" for translate file). "parts" for generate parts file. Wait gemini response then write to output_file. input_file will be DETELE! \*\* Watchout limit response text from gemini, split file base on this.

#### [process-batch.py](process-batch.py): load all part\_{number}.txt from [split-line.py](split-line.py) file and give [process.py](process.py), inteval after 3 mins (150 seconds).

#### [gen-txt-raw.py](gen-txt-raw.py): Generate txt from raw, input is 4 file [words.txt](dictionary/words.txt), [ipa.txt](dictionary/ipa.txt), [vi.txt](dictionary/vi.txt) and [parts.txt](dictionary/parts.txt). Output [data.txt](dictionary/data/data.txt).

#### [gen-json-txt.py](gen-json-txt.py): Generate json from txt, input is [data.txt](dictionary/data/data.txt) from [gen-txt-raw.py](gen-txt-raw.py). Output [data.json](dictionary/data/data.json).

#### [gen-xlsx-json.py](gen-xlsx-json.py): Generate xlsx from json, input is [data.json](dictionary/data/data.json) from [gen-json-txt.py](gen-json-txt.py). Output [data.xlsx](dictionary/data/data.xlsx).

#### [gen-pdf-json.py](gen-pdf-json.py): Generate pdf from json, input is [data.json](dictionary/data/data.json) from [gen-json-txt.py](gen-json-txt.py) Output is list pdf file named data_startword-endword.pdf each file contain 5000 words.

#### [merge-pdf.py](merge.py): Merge all pdf of [gen-pdf-json.py](gen-pdf-json.py) into single file pdf. \*\* Update pdf_order before merge. Output [data.pdf](dictionary/data/data.pdf).

## Generate data

1. Set up your API key in the [process.py](process.py) file:
   ```python
   genai.configure(api_key="YOUR_API_KEY")
   ```
2. Configure model you want use
   ```python
    model = genai.GenerativeModel(
        "gemini-2.0-flash-exp",
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            top_k=1,
            top_p=1,
        ),
    )
   ```
3. Split file with [split-line.py](split-line.py)
   ```sh
   python split-line.py
   ```
4. Run the batch to process file from [split-line.py](split-line.py)
   ```sh
   python process-batch.py
   ```

## Note

#### Prepare your file or move from [dictionary](dictionary) to root project folder. If output file have diffence name, rename it or update code. All file seperate word by new line, seperate word content by tabspace.

#### Limit number words generate, you can use [split-line.py](split-line.py) and modify end_line and lines_per_file (ex: 5000) for first 5000 words then rename file or change code base on new file name before generate txt -> json -> pdf, xlsx.

#### Currently, my project contains 53,966 words. Modify the process to limit the output to a specific number of words, such as 5,000, so the generated JSON contains only 5,000 words.

#### Data is generated by gemini. Checking carefully before use for production.

## LICENSE

This project is open-source and available under the [MIT License](LICENSE).

- Created by VeMines with love ❤️. If you like this project please star ⭐ it
