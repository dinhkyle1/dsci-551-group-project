import streamlit as st
from pymongo import MongoClient

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
st.set_page_config(page_title="Spotify Tracks Distributed Database", layout="wide")

# Function to validate input fields
def validate_input(input_data):
    errors = []
    if not input_data["track_id"]:
        errors.append("Track ID cannot be blank.")
    return errors

# Light to dark theme toggle
theme = st.sidebar.checkbox("Dark Mode", False, key="theme", help="Toggle dark mode")

# Apply dark mode theme if selected
if theme:
    st.markdown(
        """
        <style>
        /* Dark mode CSS */
        body, .stApp {
            color: #f8f9fa;
            background-color: #343a40;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Insert button and entry fields in the sidebar
with st.sidebar:
    insert_button_clicked = st.button("Insert")
    if insert_button_clicked:
        st.session_state.insert_button_clicked = True

    if st.session_state.get("insert_button_clicked"):
        st.markdown("## Insert New Record")
        with st.form(key="insert_form"):
            entry = {}
            entry["_id"] = st.text_input("Track ID")
            entry["artists"] = st.text_input("Artists")
            entry["album_name"] = st.text_input("Album Name")
            entry["track_name"] = st.text_input("Track Name")
            entry["popularity"] = st.number_input("Popularity", min_value=0, max_value=100, step=1)
            entry["danceability"] = st.slider("Danceability", min_value=0.0, max_value=1.0, step=0.01)
            entry["energy"] = st.slider("Energy", min_value=0.0, max_value=1.0, step=0.01)
            entry["key"] = st.number_input("Key", min_value=0)
            entry["loudness"] = st.slider("Loudness", min_value=-60.0, max_value=0.0, step=0.1)
            entry["mode"] = st.selectbox("Mode", [0, 1])
            entry["speechiness"] = st.slider("Speechiness", min_value=0.0, max_value=1.0, step=0.01)
            entry["acousticness"] = st.slider("Acousticness", min_value=0.0, max_value=1.0, step=0.01)
            entry["instrumentalness"] = st.slider("Instrumentalness", min_value=0.0, max_value=1.0, step=0.01)
            entry["liveness"] = st.slider("Liveness", min_value=0.0, max_value=1.0, step=0.01)
            entry["valence"] = st.slider("Valence", min_value=0.0, max_value=1.0, step=0.01)
            entry["tempo"] = st.slider("Tempo", min_value=0.0, max_value=300.0, step=1.0)
            entry["time_signature"] = st.number_input("Time Signature", min_value=3, max_value=7)
            entry["track_genre"] = st.text_input("Track Genre")
            
            submit_button_clicked = st.form_submit_button("Submit")
            
            if submit_button_clicked:
                # Validate the input
                errors = validate_input(entry)
                if errors:
                    st.error("\n".join(errors))
                else:
                    # Insert the entry into the appropriate databases
                    inserted = False
                    try:
                        # Insert into the corresponding database
                        database_key = f"song_metadata_{hash_fun(entry['track_id'])}"
                        collection = mongo_clients[database_key][database_key]["song"]
                        collection.insert_one(entry)  # Changed to insert_many
                        inserted = True
                    except Exception as e:
                        st.error(f"Error occurred: {e}")
                    
                    if inserted:
                        st.success("Insertion successful!")

# Modify button in the sidebar
with st.sidebar:
    modify_button_clicked = st.button("Modify")
    if modify_button_clicked:
        st.session_state.modify_button_clicked = True

    if st.session_state.get("modify_button_clicked"):
        st.markdown("## Modify Record")
        selected_row_id = st.text_input("Enter Track ID of the row to modify", key="selected_row_id")
        
        search_button_clicked = st.button("Search")

        if search_button_clicked:
            if not selected_row_id:
                st.error("No Track ID entered.")
            else:
                # Hash the track_id to determine which database to search
                hash_value = hash_fun(selected_row_id)
                
                # Connect to the corresponding database based on the hash value
                if hash_value == 0:
                    database = mongo_clients["song_metadata_0"]["song_metadata_0"]["song"]
                    audio_database = mongo_clients["song_metadata_0"]["audio_elements_0"]["song"]
                else:
                    database = mongo_clients["song_metadata_1"]["song_metadata_1"]["song"]
                    audio_database = mongo_clients["song_metadata_1"]["audio_elements_1"]["song"]
                    
                
                # Search for the track_id in the selected database
                selected_row = None
                data = list(database.find({"_id": selected_row_id}))
                if data:
                    selected_row = data[0]
                    print("Selected Row (Before Appending Audio Elements):", selected_row)  # Print out the selected row dictionary for inspection
                
                if selected_row:
                    # Append audio elements to the selected row
                    audio_data = audio_database.find_one({"_id": selected_row_id})
                    if audio_data:
                        for key, value in audio_data.items():
                            selected_row[key] = value
                            
                    print("Selected Row (After Appending Audio Elements):", selected_row)  # Print out the selected row dictionary for inspection
                    
                    with st.form(key="modify_form"):
                        entry = {}
                        entry["_id"] = st.text_input("Track ID", value=selected_row_id, key="track_id_modify", disabled=True)
                        entry["artists"] = st.text_input("Artists", value=selected_row.get("artists", ""), key="artists_modify")
                        entry["album_name"] = st.text_input("Album Name", value=selected_row.get("album_name", ""), key="album_name_modify")
                        entry["track_name"] = st.text_input("Track Name", value=selected_row.get("track_name", ""), key="track_name_modify")
                        entry["popularity"] = st.number_input("Popularity", value=float(selected_row.get("popularity", 0)), min_value=0.0, max_value=100.0, step=1.0, key="popularity_modify")
                        entry["danceability"] = st.slider("Danceability", value=float(selected_row.get("danceability", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="danceability_modify")
                        entry["energy"] = st.slider("Energy", value=float(selected_row.get("energy", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="energy_modify")
                        entry["key"] = st.number_input("Key", value=int(selected_row.get("key", 0)), min_value=0, key="key_modify")
                        entry["loudness"] = st.slider("Loudness", value=float(selected_row.get("loudness", -30.0)), min_value=-60.0, max_value=0.0, step=0.1, key="loudness_modify")
                        entry["mode"] = st.selectbox("Mode", options=[0, 1], index=int(selected_row.get("mode", 0)), key="mode_modify")
                        entry["speechiness"] = st.slider("Speechiness", value=float(selected_row.get("speechiness", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="speechiness_modify")
                        entry["acousticness"] = st.slider("Acousticness", value=float(selected_row.get("acousticness", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="acousticness_modify")
                        entry["instrumentalness"] = st.slider("Instrumentalness", value=float(selected_row.get("instrumentalness", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="instrumentalness_modify")
                        entry["liveness"] = st.slider("Liveness", value=float(selected_row.get("liveness", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="liveness_modify")
                        entry["valence"] = st.slider("Valence", value=float(selected_row.get("valence", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="valence_modify")
                        entry["tempo"] = st.slider("Tempo", value=float(selected_row.get("tempo", 120.0)), min_value=0.0, max_value=300.0, step=1.0, key="tempo_modify")
                        entry["time_signature"] = st.number_input("Time Signature", value=int(selected_row.get("time_signature", 4)), min_value=3, max_value=7, key="time_signature_modify")
                        entry["track_genre"] = st.text_input("Track Genre", value=selected_row.get("track_genre", ""), key="track_genre_modify")
                        
                        submit_button_clicked = st.form_submit_button("Submit")

                        if submit_button_clicked:
                            st.markdown("Submit button clicked!")  # Print statement for debugging
                            # Validate the input
                            errors = validate_input(entry)
                            if errors:
                                print("Errors:", errors)  # Debugging print statement
                                st.error("\n".join(errors))
                            else:
                                try:
                                    st.markdown("Updating database with entry:", entry)  # Debugging print statement
                                    
                                    # Update the selected row with the modifications
                                    database.update_one({"track_id": selected_row_id}, {"$set": entry})
                                    
                                    # Loop through the entry and update both collections
                                    for key, value in entry.items():
                                        # Update song_metadata collection
                                        database.update_one({"track_id": selected_row_id}, {"$set": {key: value}})
                                        
                                        # Update audio_elements collection
                                        audio_database.update_one({"_id": selected_row_id}, {"$set": {key: value}})
                                        
                                    st.success("Modification successful!")
                                except Exception as e:
                                    print("Error occurred during update:", e)  # Debugging print statement
                                    st.error("An error occurred during modification. Please try again later.")

                else:
                    st.error("Entered Track ID cannot be found in databases.")








# Display tables in a single column
for db_name, client in mongo_clients.items():
    st.markdown(f"<h2 style='color: #1DB954;'>{db_name.capitalize()} Database</h2>", unsafe_allow_html=True)

    # Choose the database and collection
    database = client[db_name]
    collection = database["song"]

   # Query data from the collection
    data = list(collection.find().limit(100))  # Displaying only the first 100 records

    # st.markdown(f'## {db_name.capitalize()} Database')

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
