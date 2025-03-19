# Duden Scraper

Duden Scraper is a Python script that fetches word definitions, examples, and meanings from the Duden website. It allows you to save selected definitions to a CSV file, which can then be imported into Anki or other flashcard applications.

## Features
- Prompts the user to enter a German word.
- Fetches dictionary entries for the word from the Duden website.
- If no direct entry is found, performs a search and allows the user to select from the top results.
- Creates cards with the word, its definition, and examples.
- Saves selected cards to a CSV file in a format compatible with Anki.

## Requirements
This script requires the following Python libraries:
- `requests`
- `beautifulsoup4`

You can install them using:
```bash
pip install requests beautifulsoup4
```

## How It Works
1. Run the script from the terminal.
2. Enter a German word when prompted.
3. The script will:
   - Try to find a dictionary entry for the word.
   - If no entry is found, perform a search on the Duden website and display the top results.
4. The script will display a list of cards in the format:
   ```
   [word, definition, examples]
   ```
5. You can select the cards you want to save by entering their numbers.
6. The selected cards will be written to a CSV file (`cards.csv`).

## Notes
- The CSV file is opened in append mode, so you may need to manually clean its contents after importing it into Anki or other tools.
- Make sure to capitalize German nouns when entering words, as the script does not handle case correction.

## Usage
Run the script from the terminal:
```bash
python duden_scraper.py
```

Follow the prompts to look up words and save cards.

## Example Workflow
1. **Input**: Enter the word `Haus`.
2. **Output**: The script fetches the dictionary entry for `Haus` or displays search results if no direct entry is found.
3. **Card Creation**: The script creates cards like:
   ```
   [Haus, "A building for living in", "Das Haus ist groß."]
   ```
4. **Save to CSV**: Select the cards you want to save, and they will be added to cards.csv.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
