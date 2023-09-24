# Take each row in favorites table and turn it in to many rows in the 
# fav_sentences table, each with a piece of text split on full stops
# and newlines

import sqlite3
import re


# connect to SQLite for writing data to disk
sqliteConnection = sqlite3.connect('favs.db')
cursor = sqliteConnection.cursor()

# pull the full text
resultset = cursor.execute("SELECT * FROM favorites;").fetchall()

# convert set to new data structure with lists instead of tuples
for i in resultset:
    intermediate_step = []
    no_double_returns = [snippet for snippet in i[2].split('\n') if snippet]
    # capture words in-between newlines and full stops
    no_full_stops = []
    no_full_stops.extend(snippet
                             for passage in no_double_returns
                                for snippet in re.split(r'[\.\?]', passage)
                                    if len(snippet) > 40)

    if no_full_stops:
        for j in no_full_stops:
            intermediate_step.append((i[1],i[0],j,))

    # insert this page's snippets into the fav_sentences table
    if intermediate_step:
        for snippet in intermediate_step:
            query = f'INSERT INTO fav_sentences (url, favorites_id, sentence) \
                    VALUES (?, ?, ?);'

            cursor.execute(query, (snippet[0], snippet[1], snippet[2],))
        sqliteConnection.commit()

cursor.close()
sqliteConnection.close()
