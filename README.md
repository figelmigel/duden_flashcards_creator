This is a Python script intended to be run from a terminal. It requires requests and beautiful soup libraries to work.
The script itself works as follows:
  1. It will prompt you for a german word
  2. It will try to find a dictionary entry related to that word
  3. If it fails, it will instead perform a search on duden website and ask you if any of the top results is what you are looking for
  4. It will print a list of cards created from the dictionary organized like this: [word, definition, examples]
  5. It will ask for numbers of cards you want to add and write them to a csv file

You can then import the csv to anki
The file is opened in append mode, which means you will have to manually clean its contents after import
