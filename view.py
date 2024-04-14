import streamlit as st
from common_ui import main_header
from mongo_utils import get_mongo_client

def show_view_page():
    #main_header()
    db_selection = st.selectbox("Select Database", ["Song Metadata", "Audio Elements"], key='db_select')
    mongo_clients = get_mongo_client()

    if db_selection == "Song Metadata":
        display_database(mongo_clients, "song_metadata_0")
        display_database(mongo_clients, "song_metadata_1")
    elif db_selection == "Audio Elements":
        display_database(mongo_clients, "audio_elements_0")
        display_database(mongo_clients, "audio_elements_1")

    # Close the MongoDB connections
    for client in mongo_clients.values():
        client.close()

def display_database(mongo_clients, db_key):
    """Displays data from the specified database in a table format."""
    client = mongo_clients[db_key]
    database = client[db_key]
    collection = database["song"]
    data = list(collection.find().limit(100))  # Displaying only the first 100 records

    if data:
        st.subheader(f"{db_key.replace('_', ' ').title()} Database")
        st.dataframe(data)

if __name__ == "__main__":
<<<<<<< HEAD
    show_view_page()
=======
    show_view_page()
>>>>>>> frontend
