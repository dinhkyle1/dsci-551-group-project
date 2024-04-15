import streamlit as st
from common_ui import main_header
from mongo_utils import get_mongo_client
from pymongo import MongoClient

def show_filter_page():
    song_metadata_cols = ["track_id", "artists", "album_name", "track_name", "track_genre"]
    audio_elements_cols = ["track_id", "popularity", "danceability", "energy", "key", "loudness",
                           "mode", "speechiness", "acousticness", "instrumentalness", "liveness",
                           "valence", "tempo", "time_signature"]
    # Hash function to determine which database to interact with based on track_id
    def hash_fun(track_id):
        return sum(ord(c) for c in track_id) % 2   
    
    # Connect to the MongoDB databases
    mongo_client = MongoClient("mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/")
    
    if "page" not in st.session_state:
        st.session_state.page = "Home"   
    
    if "page_metadata" not in st.session_state:
        st.session_state.page_metadata = "none"
    
    if "page_elements" not in st.session_state:
        st.session_state.page_elements = "none"

    st.markdown("<h1 style='text-align:center;'>Query Spotify Databases</h1>", unsafe_allow_html=True)

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
        st.session_state.page_elements = "none"
        st.markdown("<h1 style='text-align:center;'>Choose the Attribute to Query</h1>", unsafe_allow_html=True)
        
        for i in range(3):
            st.text("")
            
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
            user_input = st.text_input("Insert ID", help = "Track ID is case-sensitive")
    
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck ID</h1>", unsafe_allow_html=True)
                    
        if st.session_state.page_metadata == "artists":
            user_input = st.text_input("Insert Artist Name").lower()
    
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Artist Name</h1>", unsafe_allow_html=True)
                    
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Album Name</h1>", unsafe_allow_html=True)
                    
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Track Name</h1>", unsafe_allow_html=True)
                    
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Genre</h1>", unsafe_allow_html=True)
    
    if st.session_state.page == "Audio Elements":
        st.session_state.page_metadata = "none"
        st.markdown("<h1 style='text-align:center;'>Choose the Attribute to Query</h1>", unsafe_allow_html=True)
        
        for i in range(3):
            st.text("")
            
        col1, col2, col3, col4, col5 = st.columns(5)
        col6, col7, col8, col9, col10 = st.columns(5)
        col11, col12, col13, col14, col15 = st.columns(5)
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
            if col10.button("instrumental", help = "Query by instrumentalness"):
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
    
        if st.session_state.page_elements == "track_id":
            user_input = st.text_input("Insert ID", help = "Track ID is case-sensitive")
    
            if user_input:
                hash = hash_fun(user_input)
                if hash == 0:
                    database = mongo_client["audio_elements_0"]
                else:
                    database = mongo_client["audio_elements_1"]
    
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Track ID</h1>", unsafe_allow_html=True)
    
    
        if st.session_state.page_elements == "popularity":
            user_input = st.number_input("Insert Popularity Score", step = 1, value = None, help = "Insert a value between 0 and 100")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"popularity": user_input}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"popularity": user_input}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Popularity Score</h1>", unsafe_allow_html=True)       
    
        if st.session_state.page_elements == "danceability":
            user_input = st.number_input("Insert Danceability Score", step = 0.01, value = None, help = "Insert a number between 0 and 1")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"danceability": user_input}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"danceability": user_input}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Danceability Score</h1>", unsafe_allow_html=True)         
    
        if st.session_state.page_elements == "energy":
            user_input = st.number_input("Insert Energy Value", step = 0.01, value = None, help = "Insert a number between 0 and 1")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"energy": user_input}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"energy": user_input}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Energy Value</h1>", unsafe_allow_html=True) 
    
        if st.session_state.page_elements == "key":
            user_input = st.number_input("Insert Key", step = 1, value = None, help = "Insert a number between 0 and 11")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"key": user_input}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"key": user_input}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Key</h1>", unsafe_allow_html=True)       
    
        if st.session_state.page_elements == "loudness":
            user_input = st.number_input("Insert Loudness", step = 0.1, format="%.1f", value = None, help = "Insert a number between -30 and 10")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"loudness": {"$gte": user_input, "$lt": user_input + 0.1}}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"loudness": {"$gte": user_input, "$lt": user_input + 0.1}}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Loudness</h1>", unsafe_allow_html=True)     
    
        if st.session_state.page_elements == "mode":
            user_input = st.number_input("Insert Mode", step = 1, value = None, help = "Insert 0 or 1")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"mode": user_input}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"mode": user_input}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Mode</h1>", unsafe_allow_html=True)
    
        if st.session_state.page_elements == "speechiness":
            user_input = st.number_input("Insert Speechiness Score", step = 0.01, format="%.2f", value = None, help = "Insert a number between 0 and 1")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"speechiness": {"$gte": user_input, "$lt": user_input + 0.01}}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"speechiness": {"$gte": user_input, "$lt": user_input + 0.01}}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Speechiness Value</h1>", unsafe_allow_html=True)
    
        if st.session_state.page_elements == "acousticness":
            user_input = st.number_input("Insert Acousticness Value", step = 0.01, format="%.2f", value = None, help = "Insert a number between 0 and 1")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"acousticness": {"$gte": user_input, "$lt": user_input + 0.01}}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"acousticness": {"$gte": user_input, "$lt": user_input + 0.01}}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Acousticness Value</h1>", unsafe_allow_html=True)
    
        if st.session_state.page_elements == "instrumentalness":
            user_input = st.number_input("Insert Instrumentalness Value", step = 0.00001, format="%.5f", value = None, help = "Acceptable values are small (ex: 0.00005)")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"instrumentalness": {"$gte": user_input, "$lt": user_input + 0.00001}}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"instrumentalness": {"$gte": user_input, "$lt": user_input + 0.00001}}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Instrumentalness Value</h1>", unsafe_allow_html=True)
    
        if st.session_state.page_elements == "liveness":
            user_input = st.number_input("Insert Liveness Value", step = 0.01, format="%.2f", value = None, help = "Insert a number between 0 and 1")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"livenss": {"$gte": user_input, "$lt": user_input + 0.01}}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"liveness": {"$gte": user_input, "$lt": user_input + 0.01}}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Liveness Value</h1>", unsafe_allow_html=True)
    
        if st.session_state.page_elements == "valence":
            user_input = st.number_input("Insert Valence", step = 0.01, format="%.2f", value = None, help = "Insert a number between 0 and 1")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"valence": {"$gte": user_input, "$lt": user_input + 0.01}}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"valence": {"$gte": user_input, "$lt": user_input + 0.01}}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Valence</h1>", unsafe_allow_html=True)
    
        if st.session_state.page_elements == "tempo":
            user_input = st.number_input("Insert Tempo", step = 1, value = None, help = "Insert an integer between 80 and 150")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"tempo": {"$gte": user_input, "$lt": user_input + 1}}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"tempo": {"$gte": user_input, "$lt": user_input + 1}}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Tempo</h1>", unsafe_allow_html=True)
    
        if st.session_state.page_elements == "time_signature":
            user_input = st.number_input("Insert Time Signature", step = 1, value = None, help = "Insert 3, 4, or 5")
    
            if user_input is not None:
                database = mongo_client["audio_elements_0"]
                collection = database["song"]
        
                data0 = list(collection.find({"time_signature": user_input}))
        
                database = mongo_client["audio_elements_1"]
                collection = database["song"]
                
                data1 = list(collection.find({"time_signature": user_input}))
                
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
                    st.write("<h1 style='text-align:center;'>No Songs Found!</h1>", unsafe_allow_html=True) 
                    st.write("<h1 style='text-align:center;'>Recheck Time Signature</h1>", unsafe_allow_html=True)
    
    for i in range(5):
        st.text("")
    
    if "show_text_box" not in st.session_state:
        st.session_state.show_text_box = False
    
    
    if st.button("Generate Spotify Links"):
        st.session_state.show_text_box = True
    
    if st.session_state.show_text_box:
        spotify_ids = st.text_area("Enter Spotify IDs", help = "Keep IDs on different lines")
        spotify_ids_lst = spotify_ids.split("\n")
        empty = True
        
        if spotify_ids:
            for spotify_id in spotify_ids_lst:
                spotify_id = spotify_id.strip()
                
                hash = hash_fun(spotify_id)
                if hash == 0:
                    database = mongo_client["song_metadata_0"]
                else:
                    database = mongo_client["song_metadata_1"]
                        
                collection = database["song"]
                data = list(collection.find({"_id": spotify_id}))
                    
                if data == []:
                    empty = False
                    break
                    
            if not empty:
                st.markdown("<h1 style='text-align:center;'>Insert Valid IDs</h1>", unsafe_allow_html=True)
            else:  
                for spotify_id in spotify_ids_lst:
                    spotify_id = spotify_id.strip()
                    st.markdown(f"{spotify_id}: https://open.spotify.com/track/{spotify_id}", unsafe_allow_html = True)
    
    with col5:
        pass
    with col2:
        pass
    with col4:
        pass
    
    for i in range(5):
        st.text("")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        pass
    with col3:
        if col3.button("Restart", help = "Click this button twice to restart the query process"):
            st.session_state.page = "Home"
            st.session_state.page_metadata = "none"
            st.session_state.page_elements = "none"
            st.session_state.show_text_box = False
    with col5:
        pass
    with col2:
        pass
    with col4:
        pass


if __name__ == "__main__":
    show_filter_page()