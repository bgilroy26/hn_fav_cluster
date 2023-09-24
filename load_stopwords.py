# to pull my favorites in from Hacker News and index tokenize them
import sqlite3
import string

#connect to SQLite for writing data to disk
sqliteConnection = sqlite3.connect('favs.db')
cursor = sqliteConnection.cursor()
with open('stopwords.txt','r') as f:     
    lines = f.readlines()
    for line in lines:
        word = line.rstrip()
        query = f'INSERT INTO stop_words (word) \
                VALUES (?);'

        cursor.execute(query, (word,))

sqliteConnection.commit()
cursor.close()
sqliteConnection.close()
