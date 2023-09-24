# take the sentences in the db and generate Bert vectors
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

sqliteConnection = sqlite3.connect('favs.db')
cursor = sqliteConnection.cursor()
select_query = """SELECT * FROM fav_sentences WHERE id = 9"""
rows = cursor.execute(select_query).fetchall()
sentence_ids = [row[0] for row in rows]
sentences = [row[3] for row in rows]

sentence_embeddings = model.encode(sentences)

insert_query = """INSERT INTO sentence_vectors (sentence_id, 
"""

for i in range(383):
    insert_query += f'a{i},\n'
insert_query += "a383) VALUES("

for j in range(384):
    insert_query += '?, '
insert_query += '?);'

for sentence_id, embedding in zip(sentence_ids, sentence_embeddings):
    insert_list = [sentence_id] + embedding.tolist()
    cursor.execute(insert_query, insert_list)
    sqliteConnection.commit()
cursor.close()
sqliteConnection.close()
