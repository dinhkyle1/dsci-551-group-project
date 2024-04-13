import streamlit as st
from pymongo import MongoClient

st.set_page_config(initial_sidebar_state="collapsed")

# Hash function to determine which database to interact with based on track_id
def hash_fun(track_id):
    return sum(ord(c) for c in track_id) % 2

# Define database connection URLs with ports for each database
database_url = "mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/",


song_metadata_cols = ["track_id", "artists", "album_name", "track_name", "track_genre"]
audio_elements_cols = ["track_id", "popularity", "danceability", "energy", "key", "loudness",
                       "mode", "speechiness", "acousticness", "instrumentalness", "liveness",
                       "valence", "tempo", "time_signature"]

# Connect to the MongoDB databases
mongo_client = MongoClient(database_url)

page = st.sidebar.selectbox("Select a Database", ("Home", "Song Metadata", "Audio Elements"))

if "page" not in st.session_state:
    st.session_state.page = "Home"

page_metadata = st.sidebar.selectbox("Metadata Attributes", ("none", "track_id", "artists", "album_name", "track_name", "track_genre"))

if "page_metadata" not in st.session_state:
    st.session_state.page_metadata = "none"

page_elements = st.sidebar.selectbox("Element Attributes", ("none", "track_id", "popularity", "danceability", "energy", "key", "loudness",
                       "mode", "speechiness", "acousticness", "instrumentalness", "liveness",
                       "valence", "tempo", "time_signature"))

if "page_elements" not in st.session_state:
    st.session_state.page_elements = "none"

st.markdown("<h1 style='text-align: center;'>Query Spotify Databases</h1>", unsafe_allow_html=True)
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
    if col2.button("Query Song Metadata", help = "Click this button to query Song Metadata"):
        st.session_state.page = "Song Metadata"
with col4:
    if col4.button("Query Audio Elements", help = "Click this button to query Audio Elements"):
        st.session_state.page = "Audio Elements"

if st.session_state.page == "Song Metadata":
        
    st.markdown("<h1 style='text-align: center;'>Choose the Attribute to Query</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if col1.button("track_id", help = "Query by track_id"):
            st.session_state.page_metadata = "track_id"
    with col2:
        if col2.button("artists", help = "Query by artists"):
            st.session_state.page_metadata = "artists"
    with col3:
        if col3.button("album_name", help = "Query by album_name"):
            st.session_state.page_metadata = "album_name"
    with col4:
        if col4.button("track_name", help = "Query by track_name"):
            st.session_state.page_metadata = "track_name"
    with col5:
        if col5.button("track_genre", help = "Query by track_genre"):
            st.session_state.page_metadata = "track_genre"

    if st.session_state.page_metadata == "track_id":
        user_input = st.text_input("Insert ID")

        if user_input:
            hash = hash_fun(user_input)
            if hash == 0:
                database = mongo_client["song_metadata_0"]
            else:
                database = mongo_client["song_metadata_1"]

            collection = database["song"]
            data = list(collection.find({"_id": user_input}))

            try:
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
                
            except IndexError:
                st.write("<h1 style='text-align: center;'>No Songs Found! Recheck ID</h1>", unsafe_allow_html=True)
                
    if st.session_state.page_metadata == "artists":
        user_input = st.text_input("Insert Artist").lower()

        if user_input:
            database = mongo_client["song_metadata_0"]
            collection = database["song"]
    
            data0 = list(collection.find({"artists": {"$regex": user_input, "$options": "i"}}))
    
            database = mongo_client["song_metadata_1"]
            collection = database["song"]
            
            data1 = list(collection.find({"artists": {"$regex": user_input, "$options": "i"}}))
            
            data = data0 + data1

            # Convert data to HTML table with scrollbar
            try:
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
                
            except IndexError:
                st.write("<h1 style='text-align: center;'>No Songs Found! Recheck Artist</h1>", unsafe_allow_html=True)
    if st.session_state.page_metadata == "album_name":
        user_input = st.text_input("Insert Album Name").lower()

        if user_input:
            database = mongo_client["song_metadata_0"]
            collection = database["song"]
    
            data0 = list(collection.find({"album_name": {"$regex": "^" + user_input + "$", "$options": "i"}}))
    
            database = mongo_client["song_metadata_1"]
            collection = database["song"]
            
            data1 = list(collection.find({"album_name": {"$regex": "^" + user_input + "$", "$options": "i"}}))
            
            data = data0 + data1

            # Convert data to HTML table with scrollbar
            try:
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
                
            except IndexError:
                st.write("<h1 style='text-align: center;'>No Songs Found! Recheck Album Name</h1>", unsafe_allow_html=True)
                
    if st.session_state.page_metadata == "track_name":
        user_input = st.text_input("Insert Track Name").lower()

        if user_input:
            database = mongo_client["song_metadata_0"]
            collection = database["song"]
    
            data0 = list(collection.find({"track_name": {"$regex": "^" + user_input + "$", "$options": "i"}}))
    
            database = mongo_client["song_metadata_1"]
            collection = database["song"]
            
            data1 = list(collection.find({"track_name": {"$regex": "^" + user_input + "$", "$options": "i"}}))
            
            data = data0 + data1

            # Convert data to HTML table with scrollbar
            try:
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
                
            except IndexError:
                st.write("<h1 style='text-align: center;'>No Songs Found! Recheck Track Name</h1>", unsafe_allow_html=True)
                
    if st.session_state.page_metadata == "track_genre":
        user_input = st.text_input("Insert Genre").lower()

        if user_input:
            database = mongo_client["song_metadata_0"]
            collection = database["song"]
    
            data0 = list(collection.find({"track_genre": user_input}))
    
            database = mongo_client["song_metadata_1"]
            collection = database["song"]
            
            data1 = list(collection.find({"track_genre": user_input}))
            
            data = data0 + data1

            # Convert data to HTML table with scrollbar
            try:
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
                
            except IndexError:
                st.write("<h1 style='text-align: center;'>No Songs Found! Recheck Genre</h1>", unsafe_allow_html=True)


# page_elements = st.sidebar.selectbox("Element Attributes", ("none", "track_id", "popularity", "danceability", "energy", "key", "loudness",
#                        "mode", "speechiness", "acousticness", "instrumentalness", "liveness",
#                        "valence", "tempo", "time_signature"))

if st.session_state.page == "Audio Elements":
    st.markdown("<h1 style='text-align: center;'>Choose the Attribute to Query</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14 = st.columns(14)
    with col1:
        if col1.button("track_id", help = "Query by track_id"):
            st.session_state.page_elements = "track_id"
    with col2:
        if col2.button("popularity", help = "Query by popularity"):
            st.session_state.page_elements = "popularity"
    with col3:
        if col3.button("danceability", help = "Query by danceability"):
            st.session_state.page_elements = "danceability"
    with col4:
        if col4.button("energy", help = "Query by energy"):
            st.session_state.page_elements = "energy"
    with col5:
        if col5.button("key", help = "Query by key"):
            st.session_state.page_elements = "key"
    with col6:
        if col6.button("loudness", help = "Query by loudness"):
            st.session_state.page_elements = "loudness"
    with col7:
        if col7.button("mode", help = "Query by mode"):
            st.session_state.page_elements = "mode"
    with col8:
        if col8.button("speechiness", help = "Query by speechiness"):
            st.session_state.page_elements = "speechiness"
    with col9:
        if col9.button("acousticness", help = "Query by acousticness"):
            st.session_state.page_elements = "acousticness"   
    with col10:
        if col10.button("instrumentalness", help = "Query by instrumentalness"):
            st.session_state.page_elements = "instrumentalness"
    with col11:
        if col11.button("liveness", help = "Query by liveness"):
            st.session_state.page_elements = "liveness"  
    with col12:
        if col12.button("valence", help = "Query by valence"):
            st.session_state.page_elements = "valence"
    with col13:
        if col13.button("tempo", help = "Query by tempo"):
            st.session_state.page_elements = "tempo"      
    with col14:
        if col14.button("time_signature", help = "Query by time_signature"):
            st.session_state.page_elements = "time_signature"        

for i in range(3):
    st.text("")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    pass
with col3:
    if col3.button("Restart", help = "Click this button twice to restart the query process"):
        st.session_state.page = "Home"
        st.session_state.page_metadata = "none"
with col5:
    pass
with col2:
    pass
with col4:
    pass

# Close the connections
mongo_client.close()