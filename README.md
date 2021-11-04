# Ssimple 'site' scrapper
It's a simple web scrapper that goes through Google Search results and extracts all the links pointing to `SearchEngineJournal.`
The search queries look like:
```
site:https://www.searchenginejournal.com/ {keyword}
```
The program goes through all pages of search results until it's not pointing to the specified page anymore.

After that It saves results to csv files.

## How to use the scipt
1. You have to have a list of keywords in `keywords.txt` file
  - they have to be ordered like
  ```
    keyword1
    keyword2
    keyword3
    etc.
  ```
2. Install required packages from `requiments.txt`
3. Run the command in terminal
```
$ python main.py
```
## Future improvements
1. Add argparse to specifie:
  - the name of file with keywords
  - name of columns of csv files
  - the name of target site
  - the destination where to save our results
  - how to name our csv files
2. More complex and random sleep options to prevent Google from finding that we are using the bot
3. Add options to select how to store our results (csv, excel, txt, parquet etc.)
## The risks of using such a program
Scraping Google Search results goes against Google's terms and condiotion. Violating those can become a legal problem, but it's depends on your countries legal system.
