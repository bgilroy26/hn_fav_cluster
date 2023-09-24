# to pull my favorites in from Hacker News and index tokenize them
from bs4 import BeautifulSoup
import requests
import sqlite3
import collections
import string
import urllib.parse
import time


#### DELETE ALL DATA IN favorite_term ####
#### FIND MODEL, GET EMBEDDINGS, AND RUN SIMILARITY CLUSTERING? ####
#### k-means? ####

with open('stopwords2.txt') as e:
    stopwords = set()
    for word in e.readlines():
        stopwords.add(word.rstrip())
    
paragraph_listed = []
sqliteConnection = sqlite3.connect('favs.db')
cursor = sqliteConnection.cursor()
with open('links4.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        time.sleep(1)
        html_doc = requests.get(line.rstrip())
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        page_paragraphs = soup.find_all('p')
        
        paragraphs = []
        for para in page_paragraphs:
            paragraphs += [para.text]
        words = ''.join(paragraphs).split()

        word_counts = collections.Counter(words)

        for term in word_counts:
            all_alpha = True
            term = term.lower()

            for char in term:
                if char not in string.ascii_letters:
                    all_alpha = False

            if not all_alpha or term in stopwords:
                continue
             
            url = urllib.parse.quote(line.rstrip(), safe = '')
            query = f'INSERT INTO favorite_terms (url, term, occurrences) \
                    VALUES (?, ?, ?);'

            cursor.execute(query, (url, term, word_counts[term],))

        sqliteConnection.commit()
cursor.close()
sqliteConnection.close()
