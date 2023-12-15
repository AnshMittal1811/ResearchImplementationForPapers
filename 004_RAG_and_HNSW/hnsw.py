# -*- coding: utf-8 -*-
"""HNSW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KF3i5EQa3Z_RdvPi0Yw1rOicPlRkusHv
"""

!pip install sentence-transformers hnswlib

from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample paragraphs
paragraphs = [
    "The quick brown fox jumps over the lazy dog.",
    "Artificial Intelligence has been a subject of intrigue for decades.",
    "The history of Python dates back to the late 1980s.",
    "Machine learning and deep learning drive modern AI.",
    "Natural language processing enables computers to understand human language."
]

# Generate embeddings
embeddings = model.encode(paragraphs)

embeddings

import hnswlib

dim = embeddings.shape[1]  # Dimension of the embeddings

# Initialize the HNSWLIB index
index = hnswlib.Index(space='l2', dim=dim)

# Initialize the index
num_elements = len(paragraphs)
index.init_index(max_elements=num_elements, ef_construction=200, M=16)

# Add embeddings to the index
index.add_items(embeddings)

query_sentence = "Programming languages like Python have revolutionized software development."
query_embedding = model.encode([query_sentence])

# Query the index
k = 2  # Number of nearest neighbors
labels, distances = index.knn_query(query_embedding, k=k)

print("Query:", query_sentence)
for label, distance in zip(labels[0], distances[0]):
    print(f"Paragraph: {paragraphs[label]}, Distance: {distance}")

