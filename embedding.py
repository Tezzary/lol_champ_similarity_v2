import numpy as np
import db

num_champs = db.execute_query("SELECT COUNT(*) FROM champion")["data"][0][0]

dimensions = 15
embeddings = np.random.rand(num_champs, dimensions).astype(np.float32)
embeddings -= 0.5  # Center the embeddings around zero
embeddings /= dimensions

def get_embedding(champ_id):
    return embeddings[champ_id]

def get_similarity(champ_id1, champ_id2):
    emb1 = get_embedding(champ_id1)
    emb2 = get_embedding(champ_id2)
    return np.dot(emb1, emb2)

def get_similarity_cosine(champ_id1, champ_id2):
    emb1 = get_embedding(champ_id1)
    emb2 = get_embedding(champ_id2)
    #np.sqrt(emb1.dot(emb1) works as a normalization factor and is apparently faster than np.linalg.norm so try later
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-8)  # Adding a small epsilon to avoid division by zero

def mse_loss(label, prediction):
    return (label - prediction) ** 2

def mse_loss_derivative(label, prediction):
    return 2 * (prediction - label)

def geom_mean(mastery1, mastery2, sum_mastery):
    return np.sqrt(mastery1 * mastery2) / sum_mastery

epochs = 100
players_per_epoch = 1000
champions_per_player = 15
#epochs = 1
#players_per_epoch = 1
#champions_per_player = 2

alpha = 0.02

def dump_readable_embeddings(i):
    global embeddings
    with open(f"readable_embeddings{i}.txt", "w") as f:
        for i in range(num_champs):
            f.write(f"Champion {i}: {embeddings[i].tolist()}\n")
    print("Embeddings dumped to readable format.")

def train_embeddings():
    global embeddings
    dump_readable_embeddings(0)
    for epoch in range(epochs):
        players = db.get_players(players_per_epoch)
        for player in players:
            champions = db.get_player_champions(player['puuid'], champions_per_player)
            if len(champions) < champions_per_player:
                #print(f"Only {len(champions)} found for player: {player['puuid']}. Skipping...")
                continue

            for champ_id1 in range(champions_per_player):
                for champ_id2 in range(champ_id1 + 1, champions_per_player):
                    if champ_id1 == champ_id2:
                        continue
                    champion1 = champions[champ_id1]
                    champion2 = champions[champ_id2]
                    if champion1['i'] == None or champion2['i'] == None:
                        print(f"Champion {champion1['championName']} or {champion2['championName']} not found in database. Skipping...")
                        return
                    #print(champion1['i'], champion2['i'])
                    mastery1 = db.get_mastery(player, champion1['id'])
                    mastery2 = db.get_mastery(player, champion2['id'])
                    sum_mastery = player['totalMasteryPoints']

                    geom_mean_value = geom_mean(mastery1, mastery2, sum_mastery)
                    
                    #print(f"Geom Mean: {geom_mean_value}, Mastery1: {mastery1}, Mastery2: {mastery2}, Sum Mastery: {sum_mastery}")
                    similarity = get_similarity(champion1['i'], champion2['i'])
                    #print(f"Similarity between {champion1['championName']} and {champion2['championName']}: {similarity}")
                    #loss = mse_loss(geom_mean_value, similarity)
                    
                    loss_derivative = mse_loss_derivative(geom_mean_value, similarity)
                    if np.isnan(embeddings[champion1['i']]).any() or np.isnan(embeddings[champion2['i']]).any():
                        print(f"NaN detected in embeddings for {champion1['championName']} or {champion2['championName']}. Skipping...")
                        return
                    
                    if loss_derivative != 0:
                        #print(alpha * loss_derivative * embeddings[champions[champ_id2]['i']])
                        embeddings[champions[champ_id1]['i']] -= alpha * loss_derivative * embeddings[champions[champ_id2]['i']]
                        embeddings[champions[champ_id2]['i']] -= alpha * loss_derivative * embeddings[champions[champ_id1]['i']]
            
        print(f"Epoch {epoch + 1}/{epochs} completed.")
    dump_readable_embeddings(1)

def get_most_similar(champion_name, top_n=5):
    champion_id = db.execute_query(f"SELECT i FROM champion WHERE championName = '{champion_name}'")["data"][0][0]
    similarities = []
    for i in range(num_champs):
        if i == champion_id:
            continue
        similarity = get_similarity_cosine(champion_id, i)
        similarities.append((i, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [(db.execute_query(f"SELECT championName FROM champion WHERE i = {champ[0]}")["data"][0][0], champ[1]) for champ in similarities[:top_n]]

def load_embeddings(filename="champion_embeddings.npy"):
    global embeddings
    try:
        embeddings = np.load(filename)
        print("Embeddings loaded successfully.")
    except FileNotFoundError:
        print("Embeddings file not found. Initializing random embeddings.")
        embeddings = np.random.rand(num_champs, dimensions).astype(np.float32)

if __name__ == "__main__":
    train_embeddings()
    print("Training completed.")
    # Save embeddings to a file or database as needed
    np.save("champion_embeddings.npy", embeddings)
    # db.save_embeddings(embeddings)  # Placeholder for saving to the database