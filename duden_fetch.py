import requests
import csv
from bs4 import  BeautifulSoup



def parse_dict_entry(response):

    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    word = soup.h1.text.strip()
    
    meanings = soup.find_all(class_="enumeration__item")
    if meanings == []:
        defin = soup.find(id='bedeutung').p.text.strip()
        try:
            examples = soup.find(id='bedeutung').find(class_='note__list').text.strip()
        except AttributeError:
            examples = 'no examples'
        cards[1] = [defin, word, examples]
    else: 
        x=1
        for i in meanings:
            defin = i.find(class_='enumeration__text').text.strip()
            try:
                examples = i.find(class_="note__list").text.strip()
                examples = examples.replace('\n', '<br>')
            except AttributeError:
                examples = ''
            cards[x] = [defin, word, examples]
            x+=1
def format_examples(examples):
    pass

def get_cards_to_add(cards):

    cards_to_add = []

    for n, card in cards.items():
        print(n, ':')
        for field in card:
            print(field)
        print('\n')
    while True:
        try: 
            ncards_to_add = input('Which definitions to add? \nRespond with numbers separated by a space, 0 to add none\n>>> ').split()
            ncards_to_add = [int(num) for num in ncards_to_add]
            break
        except ValueError:
            print('Please only enter numbers')
    for n, card in cards.items():
        if n in ncards_to_add:
            cards_to_add.append(card)
    return cards_to_add

def if_not_found(word_to_fetch):
    url_search = f'https://www.duden.de/suchen/dudenonline/{word_to_fetch}'
    response_search = requests.get(url_search)
    html_search = response_search.content
    soup_search = BeautifulSoup(html_search,  "html.parser")
    results = soup_search.find_all(class_='vignette')
    if results == []:
        print('no results')
    else:
        results_options = {}
        y = 1
        for r in results[:3]:
            entry = r.h2.text.strip()
            link = r.a['href']
            snippet = r.p.text.strip()
            results_options[y] = [entry, snippet, link]
            print(y, '. ', entry,snippet, '\n')
            y+=1

        while True:
            try: 
                answer = input('Search results for your query. \nWhich of these are you interested in? (one number only)\n>>>')
                answer = int(answer)
                break
            except ValueError:
                print('Please enter one number only')
        url = f' https://www.duden.de{results_options[answer][2]}'
        response1 = requests.get(url)
    return response1


while True:
    with open('cards.csv', 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        word_to_fetch = input("Enter word to look up\nRemember to capitalize the nouns!\n>>> ")
        if word_to_fetch == 'q':
            break
        word_to_fetch = word_to_fetch.replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('ß', 'sz')
        url = 'https://www.duden.de/rechtschreibung/{}'.format(word_to_fetch)
        response = requests.get(url)

        cards = {}
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")

        try:
            word = soup.h1.text.strip()
        except AttributeError:
            response = if_not_found(word_to_fetch)

        parse_dict_entry(response)
        cards_to_add = get_cards_to_add(cards)
        csv_writer.writerows(cards_to_add)
