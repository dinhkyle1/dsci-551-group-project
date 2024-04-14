import streamlit as st
from common_ui import main_header
from mongo_utils import get_mongo_client

def show_filter_page():
    #main_header()
    db_choice = st.selectbox("Choose Database", ["Song Metadata", "Audio Elements"], key='db_choice')
    attribute = st.selectbox("Filter Attribute", get_filter_options(db_choice), key='filter_attr')
    search_query = st.text_input("Search Query", key='search_query')

    if st.button("Filter", key='filter_button'):
        mongo_clients = get_mongo_client()
        results = filter_data(mongo_clients, db_choice, attribute, search_query)
        if results:
            display_results(results)
        else:
            st.write("No results found.")
        for client in mongo_clients.values():
            client.close()

def get_filter_options(db_choice):
    if db_choice == "Song Metadata":
        return ["track_id", "artists", "album_name", "track_name", "track_genre"]
    else:
        return ["track_id", "popularity", "danceability", "energy", "key", "loudness",
                "mode", "speechiness", "acousticness", "instrumentalness", "liveness",
                "valence", "tempo", "time_signature"]

def filter_data(mongo_clients, db_choice, attribute, search_query):
    # Database query logic
    pass

def display_results(data):
    # Logic to display results
    pass

if __name__ == "__main__":
    show_filter_page()