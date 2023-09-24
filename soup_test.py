# to pull my favorites in from Hacker News and index tokenize them
from bs4 import BeautifulSoup
import requests

html_doc = requests.get('https://news.ycombinator.com/favorites?id=bgilroy26&p=' + str(1))
soup = BeautifulSoup(html_doc.text, 'html.parser')
table_data = soup.find_all('td')

for idx, cell in enumerate(table_data):
    if cell.find('a'):
        if not 'vote' in cell.find('a').get('href'):
            if not 'user' in cell.find('a').get('href'):
                print(cell.find('a').get('href'))