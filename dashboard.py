import streamlit as st
from pymongo import MongoClient

# Hash function to determine which database to interact with based on track_id
def hash_fun(track_id):
    return sum(ord(c) for c in track_id) % 2

# Define database connection URLs with ports for each database
database_urls = {
    "song_elements_0": "mongodb://3.18.103.247:27017/song_elements_0",
    "song_elements_1": "mongodb://3.18.103.247:27017/song_elements_1",
    "audio_elements_0": "mongodb://3.18.103.247:27017/audio_elements_0",
    "audio_elements_1": "mongodb://3.18.103.247:27017/audio_elements_1"
}

# Connect to the MongoDB databases
mongo_clients = {db: MongoClient(database_urls[db]) for db in database_urls}

# Streamlit UI
st.title('Spotify Tracks Distributed Database ')

# Display current data from the MongoDB databases
rows = []
for db_name in mongo_clients:
    # Connect to MongoDB 
    client = MongoClient(database_urls[db_name])
    # Choose the database
    database = client.get_default_database()
    # Choose the collection
    collection = database["song"]
    # Query data from the collection and add to rows list
    data = list(collection.find())
    rows.append([f"{db_name.capitalize()} Database"])
    print(f"First five elements in {db_name}:", data[:5])  # Print first five elements
    for item in data:
        rows.append(item)
    # Close the connection
    client.close()

# Display tables in a 2x2 grid
num_rows = len(rows)
num_cols = 2
row_index = 0
for i in range(num_rows // num_cols + 1):
    cols = st.columns(num_cols)
    for j in range(num_cols):
        if row_index < num_rows:
            if isinstance(rows[row_index], str):
                cols[j].subheader(rows[row_index])
            else:
                cols[j].table([rows[row_index]])
            row_index += 1
