# -*- coding: utf-8 -*-
"""Spotify Annoy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xD3inAgqrEuGAnUDZ4LoMKDMJKL1Dzta
"""

!pip install annoy sentence_transformers

from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

paragraphs = [
    "The quick brown fox jumps over the lazy dog.",
    "Artificial Intelligence has been a subject of intrigue for decades.",
    "The history of Python dates back to the late 1980s.",
    "Machine learning and deep learning drive modern AI.",
    "Natural language processing enables computers to understand human language.",
    "Climate change is impacting ecosystems worldwide.",
    "The exploration of Mars has revealed much about the history of the planet.",
    "Quantum computing holds the potential to revolutionize technology.",
    "Blockchain technology is transforming digital transactions.",
    "Renewable energy sources are becoming increasingly vital.",
    "The study of genetics has advanced our understanding of human health.",
    "Autonomous vehicles could reshape transportation.",
    "Virtual reality offers new possibilities in gaming and education.",
    "The Internet of Things connects everyday devices to the web.",
    "Cybersecurity is crucial in the digital age.",
    "3D printing is changing manufacturing processes.",
    "Augmented reality blends the digital and physical worlds.",
    "Big data analytics helps in understanding complex patterns.",
    "The human brain is an intricate organ still being studied.",
    "Advances in medicine are prolonging life expectancy.",
    "Robotics technology is automating various industries.",
    "Sustainable farming practices are essential for food security.",
    "The psychology of motivation is a complex study.",
    "Urban planning is key to sustainable city development.",
    "The art world continuously evolves with cultural shifts.",
    "Conservation efforts are crucial for endangered species.",
    "Space travel has always captivated human imagination.",
    "Nanotechnology is finding applications in multiple fields.",
    "Philosophy challenges our understanding of existence.",
    "Mathematics is the language of the universe.",
    "Literature reflects the human condition in diverse ways.",
    "The history of cinema offers insight into cultural changes.",
    "Music is a universal language that transcends boundaries.",
    "Photography captures moments and tells stories.",
    "Oceanography is essential for understanding marine ecosystems.",
    "Sports bring people together across the world.",
    "Cooking is both an art and a science.",
    "Fashion reflects both personal style and cultural trends.",
    "Architecture combines functionality with aesthetics.",
    "Linguistics explores the structure and evolution of language.",
    "Anthropology studies human societies and cultural diversity.",
    "The immune system is vital for human health.",
    "Astrophysics seeks to understand the universe's workings.",
    "Psychiatry plays a crucial role in mental health.",
    "Geology helps us understand Earth's history and future.",
    "The digital revolution has transformed how we communicate.",
    "Environmental science is key to addressing ecological issues.",
    "Astronomy has been practiced since ancient times.",
    "Sociology examines the behavior of societies.",
    "Biotechnology is advancing the capabilities of medical treatment."
]

embeddings = np.array(model.encode(paragraphs))

embeddings

f = embeddings.shape[1]  # Length of item vector that will be indexed
t = AnnoyIndex(f, 'angular')  # 'angular' is one of the distance metrics

for i, vector in enumerate(embeddings):
    t.add_item(i, vector)

t.build(10)  # 10 trees
t.save('test.ann')

# Load the index, if it's not in memory
u = AnnoyIndex(f, 'angular')
u.load('test.ann')

# The query
query_sentence = "Programming languages like Python have revolutionized software development."
query_embedding = model.encode([query_sentence])

query_embedding

query_embedding = query_embedding.reshape(-1)

# Ensure your query_embedding is correctly shaped
n_neighbors = 5
nearest_neighbors_indices, distances = u.get_nns_by_vector(query_embedding, n_neighbors, include_distances=True)

# Print the query and the results
print("Query:", query_sentence)
for i, (neighbor_idx, distance) in enumerate(zip(nearest_neighbors_indices, distances)):
    # Access the corresponding paragraph
    paragraph = paragraphs[neighbor_idx]
    print(f"{i + 1}: Paragraph: '{paragraph}', Distance: {distance}")

