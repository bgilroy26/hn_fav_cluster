# to pull my favorites in from Hacker News and index tokenize them
from bs4 import BeautifulSoup
import requests
import sqlite3
import urllib.parse
import time

#### IN PROGRESS, NOT READY!!! ##################
#### WHAT IS YOUR VECTORIZATION OF A PAGE??? ####
#### FIND MODEL, GET EMBEDDINGS, AND CLUSTER ####

with open('stopwords2.txt') as e:
    stopwords = set()
    for word in e.readlines():
        stopwords.add(word.rstrip())
    
paragraph_listed = []
sqliteConnection = sqlite3.connect('favs.db')
cursor = sqliteConnection.cursor()
with open('links6.txt','r') as f:
    lines = f.readlines()

    for line in lines:
        time.sleep(1)
        html_doc = requests.get(line.rstrip())
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        contents = soup.get_text()

        url = urllib.parse.quote(line.rstrip(), safe = '')
        query = f'INSERT INTO favorites (url, contents) \
                VALUES (?, ?);'

        cursor.execute(query, (url, contents,))

        sqliteConnection.commit()

cursor.close()
sqliteConnection.close()
