from typing import Iterator
from requests import get
from bs4 import BeautifulSoup
import time
import os

HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
LINK = 'www.searchenginejournal.com'

FILE_NAME = ['url_results.csv', 'keyword_counter.txt']


def create_files():
    for name in FILE_NAME:
        if not os.path.isfile(name):
            with open(name, 'w') as csv:
                pass



def read_file(path: str) -> Iterator[str]:
    with open(path) as f:
        for row in f:
            yield row.strip()

    # with open(path, 'r') as f:
    #     keywords_list = f.readlines()
    #     for i, row in enumerate(keywords_list):
    #         row = row.replace('\n', '')
    #         keywords_list[i] = row
    #
    # return keywords_list





def scraper(keyword: str):
    url = f'https://www.google.pl/search?q=site%3A+https://{LINK}/{keyword}'
    page = get(url, headers=HEADERS)
    bs = BeautifulSoup(page.text, 'html.parser')
    links = []
    count = 0
    for link in bs.find_all('div', class_='yuRUbf'):
        a_tag = link.a['href']
        validate = a_tag.split('/')[2]
        if validate == LINK:
            links.append(a_tag)
            count += 1

    # links = [link.a['href'] for link in bs.find_all('div', class_='yuRUbf')
    #          if link.a['href'].split('/')[2] == LINK]
    time.sleep(2)
    return links


def main():
    create_files()
    for keyword in read_file('keywords.txt'):
        print(scraper(keyword))
        # scraper(keyword)
        break


if __name__ == '__main__':
    main()

