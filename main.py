import csv
import os
import time
from typing import Iterator, Sequence, TypeVar, Union

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
LINK = 'www.searchenginejournal.com'
FILE_NAME = ['url_results.csv', 'keyword_counter.csv']
T = TypeVar('T', list, int)


class DataSaver:
    def __init__(self, file_name: str, header_names: Sequence[str]):
        self.file_name = file_name
        self.header_names = header_names

    def create_file(self) -> None:
        if not os.path.isfile(self.file_name):
            with open(self.file_name, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.header_names)
                writer.writeheader()

                print(f'[INFO] File {self.file_name} created')
        else:
            print(f'[INFO] File {self.file_name} already exists')

    def file_writer(self, data: Union[T], keyword: str) -> None:
        """
        Write data to file
        The sequence have to be in order
        (URL, counter)
        """
        try:
            with open(self.file_name, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.header_names)

                writer.writerow({
                    self.header_names[0]: keyword,
                    self.header_names[1]: data
                })
        except Exception as e:
            print(e)


def read_file(path: str) -> Iterator[str]:
    """Keywords loader"""
    with open(path) as f:
        for row in f:
            yield row.strip()


def scraper(keyword: str) -> Sequence[T]:
    """Scraping Bot Loop"""
    links = []
    count = 0
    page_num = 0

    while True:
        try:
            url = f'https://www.google.pl/search?q=site%3A+https://{LINK}/{keyword}&start={page_num}0'
            page = requests.get(url, headers=HEADERS)
            bs = BeautifulSoup(page.text, 'html.parser')
            
            for link in bs.find_all('div', class_='yuRUbf'):
                a_tag = link.a['href']
                validate = a_tag.split('/')[2]
                if validate == LINK:
                    links.append(a_tag)
                    count += 1
                else:
                    return (links, count)

            print(f'[INFO] Scrapped {url}')
            page_num += 1
            time.sleep(20)

        except requests.exceptions.RequestException:
            pass


def main():
    # Initialize files
    url_file = DataSaver(FILE_NAME[0], ['keyword', 'URL'])
    count_file = DataSaver(FILE_NAME[1], ['keyword', 'count'])

    # create *.csv files if does not exists
    url_file.create_file()
    count_file.create_file()

    print('[INFO] Start scraper')

    # keywords loop
    for keyword in read_file('keywords.txt'):
        data = scraper(keyword)

        url_file.file_writer(data[0], keyword)
        count_file.file_writer(data[1], keyword)

        print('[INFO] Saved URL and Count for {}'.format(keyword))


if __name__ == '__main__':
    main()
