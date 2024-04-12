import streamlit as st
from pymongo import MongoClient

st.set_page_config(initial_sidebar_state="collapsed")

# Hash function to determine which database to interact with based on track_id
def hash_fun(track_id):
    return sum(ord(c) for c in track_id) % 2

# Define database connection URLs with ports for each database
database_urls = {
    "song_metadata_0": "mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/",
    "song_metadata_1": "mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/",
    "audio_elements_0": "mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/",
    "audio_elements_1": "mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/"
}

# Connect to the MongoDB databases
mongo_clients = {db: MongoClient(database_urls[db]) for db in database_urls}

# Streamlit UI
#st.markdown('# Spotify Tracks Distributed Database Selection')

page = st.sidebar.selectbox("Select a Database", ("Home", "Song Metadata", "Audio Elements"))

if "page" not in st.session_state:
    st.session_state.page = "Home"

if page == "Home":
    #st.markdown("<h1 style='text-align: center;'>Centered Text</h1>Spotify Tracks Distributed Database Selection")
    st.markdown("<h1 style='text-align: center;'>Spotify Tracks Distributed Database Selection</h1>", unsafe_allow_html=True)
    for i in range(3):
        st.text("")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        pass
    with col3:
        pass
    with col5:
        pass
    with col2:
        if col2.button("Show Song Metadata", help = "Click this button to view Song Metadata Tables"):
            page = "Song Metadata"
    with col4:
        if col4.button("Show Audio Elements", help = "Click this button to view Audio Elements Tables"):
            page = "Audio Elements"

if page == "Song Metadata":
    st.markdown("<h1 style='text-align: center;'>Song Metadata</h1>", unsafe_allow_html=True)
    client = mongo_clients["song_metadata_0"]
    database = client["song_metadata_0"]
    # Choose the collection
    collection = database["song"]
    # Query data from the collection
    data = list(collection.find().limit(100))  # Displaying only the first 100 records

    st.markdown("<h1 style='text-align: center;'>Song Metadata 0 Database</h1>", unsafe_allow_html=True)

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

    client = mongo_clients["song_metadata_1"]
    database = client["song_metadata_1"]
    # Choose the collection
    collection = database["song"]
    # Query data from the collection
    data = list(collection.find().limit(100))  # Displaying only the first 100 records

    st.markdown("<h1 style='text-align: center;'>Song Metadata 1 Database</h1>", unsafe_allow_html=True)

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
    for i in range(3):
        st.text("")
    
    col1, col2, col3 , col4, col5 = st.columns(5)

    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        if col3.button("Remove Tables"):
            page == "Home"

if page == "Audio Elements":
    st.markdown("<h1 style='text-align: center;'>Audio Elements</h1>", unsafe_allow_html=True)
    client = mongo_clients["audio_elements_0"]
    database = client["audio_elements_0"]
    # Choose the collection
    collection = database["song"]
    # Query data from the collection
    data = list(collection.find().limit(100))  # Displaying only the first 100 records

    st.markdown("<h1 style='text-align: center;'>Audio Elements 0 Database</h1>", unsafe_allow_html=True)

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

    client = mongo_clients["audio_elements_1"]
    database = client["audio_elements_1"]
    # Choose the collection
    collection = database["song"]
    # Query data from the collection
    data = list(collection.find().limit(100))  # Displaying only the first 100 records

    st.markdown("<h1 style='text-align: center;'>Audio Elements 1 Database</h1>", unsafe_allow_html=True)

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
    
    for i in range(3):
        st.text("")
    
    col1, col2, col3 , col4, col5 = st.columns(5)

    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        if col3.button("Remove Tables"):
            page == "Home"

# Close the connections
for client in mongo_clients.values():
    client.close()
