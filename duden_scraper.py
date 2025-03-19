from bs4 import BeautifulSoup
import requests
import csv

class DudenScraper():
    '''
    A scraper for fetching word definitions, examples, and meanings from the Duden website.
    '''
    def __init__(self):
        '''
        Initializes main attributes of the class
        '''
        self.base_url = 'https://www.duden.de'
        self.search_url = 'https://www.duden.de/suchen/dudenonline/'
        self.csv_path = 'cards.csv'

    def mainloop(self):
        ''' 
        The main loop of the programm. It terminates if you press 'q' when prompted for a word
        '''
        while True:
            self.reload = False
            user_input = self.get_user_input()
            if user_input == 'q':
                break
            self.fetch_word(self.get_url(user_input))
            if self.reload:
                continue
            self.print_cards()
            self.get_cards_to_add()
            self.write_cards_to_csv()


    def get_user_input(self):
        '''
        Prompts user to enter a german word or 'q' to quit the program
        '''
        self.word_to_fetch = input(
            "Enter word to look up, q to quit \
            \nRemember to capitalize the nouns!\n>>> "
            )
        self.word_to_fetch = (
            self.word_to_fetch.replace('ä', 'ae').replace('ü', 'ue')
            .replace('ö', 'oe').replace('ß', 'sz')
            )
        return self.word_to_fetch

    def get_url(self, user_input):
        '''
        Returns an url created from the word entered
        '''
        return f'{self.base_url}/rechtschreibung/{self.word_to_fetch}'

    def fetch_word(self, url):
        '''
        Fetches the HTML content of the given URL and parses it with BeautifulSoup.
        Calls `search_word` if no main heading is found, otherwise calls `parse_word`.
        '''
        response = requests.get(url)        
        self.soup = BeautifulSoup(response.content, "html.parser")
        if self.soup.h1 == None:
            self.search_word()
        else:
            self.parse_word()
    
    def parse_word(self):
        '''
        Creates cards from 'self.soup' and adds them to the dictionary 'cards'.
        Each card is a list containing the definition, word itself, and examples.
        '''
        self.cards = {}
        word = self.soup.h1.text.strip()
        meanings = self.soup.find_all(class_="enumeration__item")
        
        if not meanings:
            # Handle case where no meanings are found
            defin = self.get_single_definition()
            examples = self.get_examples()
            self.cards[1] = [defin, word, examples]
        else:
            # Handle case where multiple meanings are found
            for i, meaning in enumerate(meanings, start=1):
                defin = self.get_meaning_text(meaning)
                examples = self.get_meaning_examples(meaning)
                self.cards[i] = [defin, word, examples]

    def get_single_definition(self):
        '''
        Extracts a single definition from the page.
        '''
        try:
            return self.soup.find(id='bedeutung').p.text.strip()
        except AttributeError:
            try:
                return (
                    self.soup.select('#bedeutung > dl:nth-child(2) > dt:nth-child(1)')[0].text + ' ' +
                    self.soup.select('#bedeutung > dl:nth-child(2) > dd:nth-child(2) > a:nth-child(1)')[0].text
                )
            except (AttributeError, IndexError):
                return 'no definition available'

    def get_examples(self):
        '''
        Extracts examples from the page.
        '''
        try:
            return self.soup.find(id='bedeutung').find(class_='note__list').text.strip()
        except AttributeError:
            return ''

    def get_meaning_text(self, meaning):
        '''
        Extracts the text of a meaning.
        '''
        try:
            return meaning.find(class_='enumeration__text').text.strip()
        except AttributeError:
            return 'no definition available'

    def get_meaning_examples(self, meaning):
        '''
        Extracts examples for a specific meaning.
        '''
        try:
            examples = meaning.find(class_="note__list").text.strip()
            return examples.replace('\n', '<br>')
        except AttributeError:
            return ''

    def search_word(self):
        '''
        Tries to find entries related to the word entered by user. If there are none reloads the main loop.
        If there are any calls print_search_results method
        '''
        url_search = f'{self.base_url}/suchen/dudenonline/{self.word_to_fetch}'
        response_search = requests.get(url_search)
        soup_search = BeautifulSoup(response_search.content, "html.parser")
        self.search_results = soup_search.find_all(class_='vignette')
        if self.search_results == []:
            print('Could not find related entries')
            self.reload = True
        else:
            self.print_search_results()

    def print_search_results(self):
        '''
        Prints enumerated search results and calls self.search_results_options method
        '''
        self.result_links = {}
        for i, result in enumerate(self.search_results[:3], start=1):
            entry = result.h2.text.strip()
            link = result.a['href']
            snippet = result.p.text.strip()
            self.result_links[i] = link
            print(i, '. ', entry,snippet, '\n')
        self.search_results_options()

    def search_results_options(self):
        '''
        Promts the user to chose a word from the the list created by 'search_word' method.
        If they choose one calls fetch_word method on it.
        If they enter 0 or other invalid number reloads the main loop.
        '''
        while True:
            try: 
                answer = int(input('''
                    Search results for your query. \nWhich of these are you interested in?
                    (one number only, 0 if none) \n>>>
                    '''))
                break
            except ValueError:
                print('Please enter one number only')
        if 0 < answer <= len(self.result_links):
            url = f' https://www.duden.de{self.result_links[answer]}'
            self.fetch_word(url)
        else: 
            self.reload = True

    def print_cards(self):
        '''
        Prints the cards made from available definitions
        '''
        for n, card in self.cards.items():
            print(n, ':')
            for field in card:
                print(field)
            print('\n')

    def get_cards_to_add(self):
        '''
        Promts the user to choose cards from those printed by the 'print_cards' function
        and saves them to the 'self.cards_to_add' list
        '''
        self.cards_to_add = []
        while True:
            try: 
                nums_of_cards_to_add = input('Which definitions to add? \
                    \nRespond with numbers separated by a space, 0 to add none\n>>> ').split()
                nums_of_cards_to_add = [int(num) for num in nums_of_cards_to_add]
                break
            except ValueError:
                print('Please only enter numbers')
        for n, card in self.cards.items():
            if n in nums_of_cards_to_add:
                self.cards_to_add.append(card)

    def write_cards_to_csv(self):
        '''
        Writes cards chosen by user to a file, specified by 'self.csv_path' attribute
        '''
        try: 
            with open(self.csv_path, 'a', encoding='utf-8', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerows(self.cards_to_add)
        except (FileNotFoundError):
            with open(self.csv_path, 'w', encoding='utf-8', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerows(self.cards_to_add)


def main():
    scraper = DudenScraper()
    scraper.mainloop()

if __name__ == '__main__':
    main()
