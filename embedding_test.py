import embedding

embedding.load_embeddings()
print(embedding.embeddings)
print(embedding.get_most_similar("Yone", 5))