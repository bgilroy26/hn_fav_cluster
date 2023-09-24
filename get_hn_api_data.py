import sqlite3
import requests
from bs4 import BeautifulSoup
import itertools
import urllib.parse
import time
import types

def item_generator(json_input):
    if isinstance(json_input, dict):
        yield json_input
        if 'children' in json_input:
            for child in json_input['children']:
                yield item_generator(child)
    elif isinstance(json_input, list):
        for item in json_input:
            yield item
            if 'children' in item:
                yield item_generator(item['children'])

sqliteConnection = sqlite3.connect('favs.db')
cursor = sqliteConnection.cursor()

with open('hn_link_ids.txt') as f:
    lines = f.readlines()
    for line in lines:
        time.sleep(1)
        line = line.rstrip()

        url = urllib.parse.quote('https://news.ycombinator.com/item?id='+line, safe='')

        response = requests.get('http://hn.algolia.com/api/v1/items/'+line)
        json = response.json()

        text = ''
        for item in item_generator(json):
            if isinstance(item, types.GeneratorType):
                for comment in item:
                    if isinstance(comment, types.GeneratorType):
                        for missive in comment:
                            if isinstance(missive, types.GeneratorType):
                                for letter in missive:
                                    if isinstance(letter, dict):
                                        if 'text' in letter and letter['text'] and len(letter['text']) > 0:
                                            text += '\n' + BeautifulSoup(letter['text'], 'html.parser').get_text()
                            if isinstance(missive, dict):
                                if 'text' in missive and missive['text'] and len(missive['text']) > 0:
                                    text += '\n' + BeautifulSoup(missive['text'], 'html.parser').get_text()
                    if isinstance(comment, dict):
                        if 'text' in comment and comment['text'] and len(comment['text']) > 0:
                            text += '\n' + BeautifulSoup(comment['text'], 'html.parser').get_text()

            #import pdb; pdb.set_trace()
            if isinstance(item, dict):
                if 'text' in item and item['text'] and len(item['text']) > 0:
                    text += '\n' + BeautifulSoup(item['text'], 'html.parser').get_text()

        query = f'INSERT INTO favorites(url, contents) \
                    VALUES (?, ?);'

        cursor.execute(query, (url, text,))

        sqliteConnection.commit()

cursor.close()
sqliteConnection.close()
