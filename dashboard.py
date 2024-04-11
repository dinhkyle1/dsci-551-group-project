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

# Function to validate input fields
def validate_input(input_data):
    errors = []
    if not input_data["track_id"]:
        errors.append("Track ID cannot be blank.")
    return errors

# Insert button and entry fields in the sidebar
with st.sidebar:
    insert_button_clicked = st.button("Insert")
    if insert_button_clicked:
        st.session_state.insert_button_clicked = True

    if st.session_state.get("insert_button_clicked"):
        st.markdown("## Insert New Record")
        with st.form(key="insert_form"):
            entry = {}
            entry["track_id"] = st.text_input("Track ID")
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
                        collection = mongo_clients[database_key]["song"]
                        collection.insert_many([entry])  # Changed to insert_many
                        inserted = True
                    except Exception as e:
                        st.error(f"Error occurred: {e}")
                    
                    if inserted:
                        st.success("Insertion successful!")

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
