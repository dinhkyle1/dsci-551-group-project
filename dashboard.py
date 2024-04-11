import streamlit as st
from pymongo import MongoClient
from streamlit_option_menu import option_menu


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
st.set_page_config(page_title="Spotify Tracks Distributed Database", layout="wide")

# Sidebar for theme selection
with st.sidebar:
    theme = option_menu("Theme", ["Light", "Dark"], icons=["sun", "moon"], menu_icon="list", default_index=0)

# Set theme
if theme == "Dark":
    st.markdown(
        """
        <style>
        /* Main background */
        body, html, .stApp, .streamlit-container {
            color: #1DB954 !important;
            background-color: #191414 !important;
        }
        /* Streamlit elements and widgets background */
        .stTextInput input, .stSelectbox select, .stSlider .slider, .stButton > button, .stSidebar > div, .stSelectbox .css-2b097c-container, .stSelectbox .css-yt9ioa-control {
            background-color: #191414 !important;
            color: #1DB954 !important;
            border-color: #1DB954;
        }
        /* Headers and Text */
        h1, h2, h3, h4, h5, h6, label, p, .stSlider label, .stMarkdown, .streamlit-expanderHeader, .stDownloadButton, .stSidebar .sidebar-content, .stSelectbox .css-1uccc91-singleValue {
            color: #1DB954 !important;
        }
        /* Streamlit's table (dataframe) styling */
        .stTable, .table {
            color: #1DB954 !important;
            background-color: #191414 !important;
        }
        /* Streamlit's select dropdown styling */
        .stSelectbox .css-2b097c-container .css-1uccc91-singleValue, .stSelectbox .css-yt9ioa-control {
            background-color: #191414 !important;
            color: #1DB954 !important;
            border-color: #1DB954;
        }
        .stSelectbox .css-1okebmr-indicatorSeparator {
            background-color: #191414 !important;
        }
        .stSelectbox .css-1hwfws3 {
            background-color: #191414 !important;
            color: #1DB954 !important;
        }
        /* Dropdown menu styling */
        .stSelectbox .css-26l3qy-menu {
            background-color: #191414 !important;
            color: #1DB954 !important;
        }
        /* Streamlit's select dropdown option hover styling */
        .stSelectbox .css-26l3qy-menu .css-9gakcf-option {
            background-color: #191414 !important;
            color: #1DB954 !important;
        }
        .stSelectbox .css-26l3qy-menu .css-9gakcf-option:hover {
            background-color: #1DB954 !important;
            color: #191414 !important;
        }
        /* Streamlit's dataframe/table styling */
        .dataframe, .dataframe tbody, .dataframe tr, .dataframe th, .dataframe td, .table, .table td, .table th, .stTable {
            color: #1DB954 !important;
            background-color: #191414 !important;
            border: 1px solid #1DB954 !important;
        }
        .stTable tr:hover {
            background-color: rgba(29, 185, 84, 0.2) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<h1 style='text-align: center; color: #1DB954;'>Spotify Tracks Distributed Database</h1>", unsafe_allow_html=True)

# Filter options
filter_options = ["Track Name", "Artist", "Genre"]
selected_filter = st.selectbox("Filter By:", filter_options)

# Search box
search_query = st.text_input("Search:", "")

# Display tables with pagination and filter
for db_name, client in mongo_clients.items():
    st.markdown(f"<h2 style='color: #1DB954;'>{db_name.capitalize()} Database</h2>", unsafe_allow_html=True)

    # Choose the database and collection
    database = client[db_name]
    collection = database["song"]

    # Filter and search
    if selected_filter == "Track Name":
        filter_key = "track_name"
    elif selected_filter == "Artist":
        filter_key = "artist_name"
    elif selected_filter == "Genre":
        filter_key = "genre"

    query = {filter_key: {"$regex": search_query, "$options": "i"}} if search_query else {}

    # Pagination controls
    total_records = collection.count_documents(query)
    page_size = 10
    total_pages = (total_records + page_size - 1) // page_size
    page_num = st.slider(f"Page (Total: {total_pages})", 1, total_pages, 1, key=db_name)

    # Query paginated data
    skip_records = (page_num - 1) * page_size
    data = list(collection.find(query).skip(skip_records).limit(page_size))

    # Display data as a table
    if data:
        st.table(data)
    else:
        st.write("No data available.")

# Close the connections
for client in mongo_clients.values():
    client.close()

