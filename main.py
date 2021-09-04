from typing import Iterator, Sequence, TypeVar
from requests import get
from bs4 import BeautifulSoup
import time
import os
import csv

HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
LINK = 'www.searchenginejournal.com'

FILE_NAME = ['url_results.csv', 'keyword_counter.csv']

T = TypeVar('T', list, int)


def create_url_file() -> None:
    """Create url_results.csv file if not exists"""
    if not os.path.isfile(FILE_NAME[0]):
        with open(FILE_NAME[0], 'a', newline='') as csvfile:
            fieldnames = ['keyword', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()


def create_count_file() -> None:
    """Create keyword_counter.csv file if not exists"""
    if not os.path.isfile(FILE_NAME[1]):
        with open(FILE_NAME[1], 'a', newline='') as csvfile:
            fieldnames = ['keyword', 'count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


def file_writer(data: Sequence[T], keyword: str) -> None:
    """
    Write data to files
    The sequence have to be in order
    (URL, counter)
    """
    with open(FILE_NAME[0], 'a', newline='') as csvfile:
        fieldnames = ['keyword', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({fieldnames[0]: keyword, fieldnames[1]: data[0]})

    with open(FILE_NAME[1], 'a', newline='') as csvfile:
        fieldnames = ['keyword', 'count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({fieldnames[0]: keyword, fieldnames[1]: data[1]})


def read_file(path: str) -> Iterator[str]:
    """Keywords loader"""
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
    return (links, count)


def main():
    create_files()
    print('[INFO] Start wraper')
    for keyword in read_file('keywords.txt'):
        data = scraper(keyword)
        file_writer(data, keyword)
        print('[INFO] Saved URL for {}'.format(keyword))


if __name__ == '__main__':
    main()
