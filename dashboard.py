import streamlit as st
from pymongo import MongoClient

# Hash function to determine which database to interact with based on track_id
def hash_fun(track_id):
    return sum(ord(c) for c in track_id) % 2

# Define database connection URLs with ports for each database
database_urls = {
    "song_metadata_0": "mongodb://Dsci-551:Dsci-551@3.18.103.247:27017/",
    "song_metadata_1": "mongodb://Dsci-551:Dsci-551@3.18.103.247:27017/",
    "audio_elements_0": "mongodb://Dsci-551:Dsci-551@3.18.103.247:27017/",
    "audio_elements_1": "mongodb://Dsci-551:Dsci-551@3.18.103.247:27017/"
}

# Connect to the MongoDB databases
mongo_clients = {db: MongoClient(database_urls[db]) for db in database_urls}

# Streamlit UI
st.markdown('# Spotify Tracks Distributed Database')

# Display tables in a single column
for db_name, client in mongo_clients.items():
    # Choose the database
    database = client[db_name]
    # Choose the collection
    collection = database["song"]
    # Query data from the collection
    data = list(collection.find().limit(100))  # Displaying only the first 100 records

    st.markdown(f'## {db_name.capitalize()} Database')

    # Convert data to HTML table with scrollbar
    html_table = f"<div style='max-height:400px; max-width:1200px; overflow:auto;'><table style='width:100%;'>"
    html_table += "<tr>"
    for col in data[0]:
        html_table += f"<th>{col}</th>"
    html_table += "</tr>"
    for row in data:
        html_table += "<tr>"
        for val in row.values():
            html_table += f"<td>{val}</td>"
        html_table += "</tr>"
    html_table += "</table></div>"

    st.write(html_table, unsafe_allow_html=True)

# Close the connections
for client in mongo_clients.values():
    client.close()
