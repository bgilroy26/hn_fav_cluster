# take sentence vectors from db and convert them to topics using berttopic 
# with all default settings
import sqlite3
import numpy as np
from bertopic import BERTopic
import sys

sqliteConnection = sqlite3.connect('favs.db')
cursor = sqliteConnection.cursor()
select_query = """
        SELECT * 
        FROM sentence_vectors sv 
        JOIN fav_sentences fs 
            ON sv.sentence_id = fs.id 
        WHERE fs.favorites_id IN (8,9);
    """
rows = cursor.execute(select_query).fetchall()
sentences = [row[389] for row in rows]
embeddings = []
for row in rows:
    embedding = []
    #numpy version
    for i in range(2, 386):
        embedding.append(np.float32(row[i]))
    embeddings.append(np.array(embedding))
embeddings = np.array(embeddings)
from bertopic.dimensionality import BaseDimensionalityReduction
from hdbscan import HDBSCAN

hdbscan_model = HDBSCAN(min_cluster_size=2, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
# Fit BERTopic without actually performing any dimensionality reduction
empty_dimensionality_model = BaseDimensionalityReduction()
topic_model = BERTopic(umap_model=empty_dimensionality_model, hdbscan_model=hdbscan_model)
topics, probs = topic_model.fit_transform(sentences, embeddings)
print(topic_model.get_topic_info())
