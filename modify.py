import streamlit as st
from common_ui import main_header
from mongo_utils import get_mongo_client
from pymongo import MongoClient

def show_crud_operations():
    if "submit_modifications_button_clicked" not in st.session_state:
        st.session_state.submit_modifications_button_clicked = False

    if "submit_button_clicked" not in st.session_state:
        st.session_state.submit_button_clicked = False

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

    # # Streamlit UI
    # st.set_page_config(page_title="Spotify Tracks Distributed Database", layout="wide")

    # Function to validate input fields
    def validate_input(input_data):
        errors = []
        if not input_data["_id"]:
            errors.append("Track ID cannot be blank.")
        return errors

    # # Light to dark theme toggle
    # theme = st.sidebar.checkbox("Dark Mode", False, key="theme", help="Toggle dark mode")

    # # Apply dark mode theme if selected
    # if theme:
    #     st.markdown(
    #         """
    #         <style>
    #         /* Dark mode CSS */
    #         body, .stApp {
    #             color: #f8f9fa;
    #             background-color: #343a40;
    #         }
    #         </style>
    #         """,
    #         unsafe_allow_html=True,
    #     )

    # Insert button and entry fields in the sidebar
    with st.sidebar:
        insert_button_clicked = st.button("Insert")
        if insert_button_clicked:
            st.session_state.submit_modifications_button_clicked = False
            st.session_state.submit_button_clicked = False
            st.session_state.modify_button_clicked = False
            st.session_state.entry1 = {}
            st.session_state.delete_button_clicked = False
            st.session_state.insert_button_clicked = True

        if st.session_state.get("insert_button_clicked"):
            st.markdown("## Insert New Record")
            entry = {}
            entry["_id"] = st.text_input("Track ID")
            entry["artists"] = st.text_input("Artists")
            entry["album_name"] = st.text_input("Album Name")
            entry["track_name"] = st.text_input("Track Name")
            entry["track_genre"] = st.text_input("Track Genre")
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
            
            submit_button_clicked = st.button("Submit", key="Insert_submit")
            
            if submit_button_clicked:
                # Validate the input
                errors = validate_input(entry)
                if errors:
                    st.error("\n".join(errors))
                else:
                    try:
                        # Determine the database keys based on the hash_fun of track_id
                        database_key = f"song_metadata_{hash_fun(entry['_id'])}"
                        audio_database_key = f"audio_elements_{hash_fun(entry['_id'])}"
                        
                        # Connect to the corresponding databases
                        song_database = mongo_clients[database_key][database_key]["song"]
                        audio_database = mongo_clients[audio_database_key][audio_database_key]["song"]
                        
                        # Insert song metadata keys into the song_metadata database
                        song_metadata_keys = ["_id", "artists", "album_name", "track_name", "track_genre"]
                        song_metadata_updates = {key: entry[key] for key in song_metadata_keys}
                        song_database.insert_one(song_metadata_updates)
                        
                        # Insert audio elements keys into the audio elements database
                        audio_elements_keys = ["_id", "popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature"]
                        audio_elements_updates = {key: entry[key] for key in audio_elements_keys}
                        audio_database.insert_one(audio_elements_updates)
                        
                        st.success(f"Inserted successfully into song_metadata_{hash_fun(entry['_id'])}!")
                        st.success(f"Inserted successfully into audio_elements_{hash_fun(entry['_id'])}!")
                    except Exception as e:
                        st.error(f"Error occurred: {e}")


    # Modify button in the sidebar
    with st.sidebar:
        modify_button_clicked = st.button("Modify")
        if modify_button_clicked:
            st.session_state.submit_button_clicked = False
            st.session_state.insert_button_clicked = False
            st.session_state.delete_button_clicked = False
            st.session_state.modify_button_clicked = True

        if st.session_state.get("modify_button_clicked"):
            st.markdown("## Modify Record")
            # with st.form(key="modify_form"):
            modify = st.radio("Modify Rows", ["Modify Single Row", "Modify Multiple Rows"])
            # modify_single_row = st.radio("Modify Single Row")
            # modify_bulk_rows = st.radio("Modify Multiple Rows")
            submit_button_clicked = False
        
            if modify == "Modify Single Row":
                selected_row_id = st.text_input("Enter Track ID of the row to modify", key="selected_row_id")
                submit_button_clicked = st.button("Submit", key="Modify_submit")

            if modify == "Modify Multiple Rows":
                attribute_to_modify = st.selectbox("Select attribute to modify rows by", ["artists", "album_name", "track_name", "popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature", "track_genre"])
                from_value = st.text_input(f"Enter 'from' value for {attribute_to_modify}", key="from_value")
                to_value = st.text_input(f"Enter 'to' value for {attribute_to_modify}", key="to_value")
                submit_button_clicked = st.button("Submit", key="Modify_submit")


            if submit_button_clicked:
                st.session_state.submit_button_clicked = True
            if st.session_state.submit_button_clicked:
                if modify == "Modify Single Row":
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
                                
                                with st.form(key="modify_form_single"):
                                    # Initialize entry1 if it's not in session state yet
                                    if "entry1" not in st.session_state:
                                        st.session_state.entry1 = {}
                                    
                                    entry1 = st.session_state.entry1
                                    
                                    entry1["_id"] = st.text_input("Track ID", value=selected_row_id, key="track_id_modify_single", disabled=True)
                                    entry1["artists"] = st.text_input("Artists", value=selected_row.get("artists", ""), key="artists_modify_single")
                                    entry1["album_name"] = st.text_input("Album Name", value=selected_row.get("album_name", ""), key="album_name_modify_single")
                                    entry1["track_name"] = st.text_input("Track Name", value=selected_row.get("track_name", ""), key="track_name_modify_single")
                                    entry1["track_genre"] = st.text_input("Track Genre", value=selected_row.get("track_genre", ""), key="track_genre_modify_single")
                                    entry1["popularity"] = st.number_input("Popularity", value=float(selected_row.get("popularity", 0)), min_value=0.0, max_value=100.0, step=1.0, key="popularity_modify_single")
                                    entry1["danceability"] = st.slider("Danceability", value=float(selected_row.get("danceability", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="danceability_modify_single")
                                    entry1["energy"] = st.slider("Energy", value=float(selected_row.get("energy", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="energy_modify_single")
                                    entry1["key"] = st.number_input("Key", value=int(selected_row.get("key", 0)), min_value=0, key="key_modify_single")
                                    entry1["loudness"] = st.slider("Loudness", value=float(selected_row.get("loudness", -30.0)), min_value=-60.0, max_value=0.0, step=0.1, key="loudness_modify_single")
                                    entry1["mode"] = st.selectbox("Mode", options=[0, 1], index=int(selected_row.get("mode", 0)), key="mode_modify_single")
                                    entry1["speechiness"] = st.slider("Speechiness", value=float(selected_row.get("speechiness", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="speechiness_modify_single")
                                    entry1["acousticness"] = st.slider("Acousticness", value=float(selected_row.get("acousticness", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="acousticness_modify_single")
                                    entry1["instrumentalness"] = st.slider("Instrumentalness", value=float(selected_row.get("instrumentalness", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="instrumentalness_modify_single")
                                    entry1["liveness"] = st.slider("Liveness", value=float(selected_row.get("liveness", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="liveness_modify_single")
                                    entry1["valence"] = st.slider("Valence", value=float(selected_row.get("valence", 0.5)), min_value=0.0, max_value=1.0, step=0.01, key="valence_modify_single")
                                    entry1["tempo"] = st.slider("Tempo", value=float(selected_row.get("tempo", 120.0)), min_value=0.0, max_value=300.0, step=1.0, key="tempo_modify_single")
                                    entry1["time_signature"] = st.number_input("Time Signature", value=int(selected_row.get("time_signature", 4)), min_value=3, max_value=7, key="time_signature_modify_single")
                                    print("After entry field section")  # Print statement for debugging

                                    submit_modifications_button_clicked = st.form_submit_button("Submit Modifications")
                                    if submit_modifications_button_clicked:
                                        st.session_state.submit_modifications_button_clicked = True
                                        print(st.session_state.get("submit_modifications_button_clicked"))

                                    # st.session_state.submit_modifications_button_clicked = True
                                        if st.session_state.get("submit_modifications_button_clicked"):
                                            print("submit_modifications_button_clicked: ", submit_modifications_button_clicked)
                                            st.session_state.submit_modifications_button_clicked = False
                                            print("Submit button clicked!")  # Print statement for debugging
                                            # Validate the input
                                            print("entry1 before modifications:", entry1)
                                            errors = validate_input(entry1)
                                            if errors:
                                                print("Errors:", errors)  # Debugging print statement
                                                st.error("\n".join(errors))
                                            else:
                                                try:
                                                    # Update entry1 with user input
                                                    entry1["_id"] = selected_row_id
                                                    entry1["artists"] = st.session_state.entry1["artists"]
                                                    entry1["album_name"] = st.session_state.entry1["album_name"]
                                                    entry1["track_name"] = st.session_state.entry1["track_name"]
                                                    entry1["track_genre"] = st.session_state.entry1["track_genre"]
                                                    entry1["popularity"] = st.session_state.entry1["popularity"]
                                                    entry1["danceability"] = st.session_state.entry1["danceability"]
                                                    entry1["energy"] = st.session_state.entry1["energy"]
                                                    entry1["key"] = st.session_state.entry1["key"]
                                                    entry1["loudness"] = st.session_state.entry1["loudness"]
                                                    entry1["mode"] = st.session_state.entry1["mode"]
                                                    entry1["speechiness"] = st.session_state.entry1["speechiness"]
                                                    entry1["acousticness"] = st.session_state.entry1["acousticness"]
                                                    entry1["instrumentalness"] = st.session_state.entry1["instrumentalness"]
                                                    entry1["liveness"] = st.session_state.entry1["liveness"]
                                                    entry1["valence"] = st.session_state.entry1["valence"]
                                                    entry1["tempo"] = st.session_state.entry1["tempo"]
                                                    entry1["time_signature"] = st.session_state.entry1["time_signature"]

                                                    # Update the selected row with the modifications
                                                    print("entry1 after modifications:", entry1)
                                                    print("right before song_metadata updates")
                                                    song_metadata_keys = ["_id", "artists", "album_name", "track_name", "track_genre"]
                                                    audio_elements_keys = [key for key in entry1.keys() if key not in song_metadata_keys]
                                                    song_metadata_updates = {key: entry1[key] for key in song_metadata_keys}
                                                    print("song_metadata_updates: ", song_metadata_updates)
                                                    audio_elements_updates = {key: entry1[key] for key in audio_elements_keys}
                                                    print("audio_elements_updates: ", audio_elements_updates)
                                                    database.update_one({"_id": selected_row_id}, {"$set": song_metadata_updates})
                                                    audio_database.update_one({"_id": selected_row_id}, {"$set": audio_elements_updates})
                                                    
                                                    st.success("Modification successful!")
                                                except Exception as e:
                                                    print("Error occurred during update:", e)  # Debugging print statement
                                                    st.error("An error occurred during modification. Please try again later.")



                elif modify == "Modify Multiple Rows":
                    if not from_value or not to_value:
                        st.error("Both 'from' and 'to' values are required.")
                    else:
                        try:
                            # from_value = float(from_value)
                            # to_value = float(to_value)
                            # Determine which database to search based on the attribute hash
                            if attribute_to_modify in ["artists", "album_name", "track_name", "track_genre"]:
                                database_keys = [f"song_metadata_{i}" for i in range(2)]
                                # sister_database_keys = [f"audio_elements_{i}" for i in range(2)]

                            if attribute_to_modify in ["popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature"]:
                                from_value = float(from_value)
                                to_value = float(to_value)
                                database_keys = [f"audio_elements_{i}" for i in range(2)]
                                # sister_database_keys = [f"song_metadata_{i}" for i in range(2)]

                            for i in range(2):
                                collection = mongo_clients[database_keys[i]][database_keys[i]]["song"]
                                # Store track IDs before modification
                                # modified_track_ids = [doc['_id'] for doc in collection.find({attribute_to_modify: {"$gte": from_value, "$lte": to_value}})]
                                # Print modified track IDs
                                # print("Modified Track IDs:", modified_track_ids)
                                # Modify the rows in the database
                                result = collection.update_many({attribute_to_modify: from_value}, {"$set": {attribute_to_modify: to_value}})
                                st.success(f"{result.modified_count} rows modified successfully in {database_keys[i]}!")
                                
                                # # Modify the rows in the sister database
                                # sister_collection = mongo_clients[sister_database_keys[i]][sister_database_keys[i]]["song"]
                                # sister_result = sister_collection.update_many({"_id": {"$in": modified_track_ids}}, {"$set": {attribute_to_modify: to_value}})
                                # st.success(f"{sister_result.modified_count} rows modified successfully in {sister_database_keys[i]}!")
                            
                        except Exception as e:
                            st.error(f"An error occurred: {e}")




    # Delete button in the sidebar
    with st.sidebar:
        delete_button_clicked = st.button("Delete")
        if delete_button_clicked:
            st.session_state.submit_modifications_button_clicked = False
            st.session_state.submit_button_clicked = False
            st.session_state.insert_button_clicked = False
            st.session_state.modify_button_clicked = False
            st.session_state.entry1 = {}
            st.session_state.delete_button_clicked = True

        if st.session_state.get("delete_button_clicked"):
            st.markdown("## Delete Record")
            # with st.form(key="delete_form"):
            modify = st.radio("Delete Rows", ["Delete Single Row", "Delete Multiple Rows"])
            # delete_single_row = st.checkbox("Delete Single Row")
            # delete_bulk_rows = st.checkbox("Delete Multiple Rows")
            
            if modify == "Delete Single Row":
                track_id_to_delete = st.text_input("Enter Track ID to delete", key="track_id_to_delete")
                delete_button = st.button("Submit", key="Delete_submit")

                
            if modify == "Delete Multiple Rows":
                attribute_to_delete = st.selectbox("Select attribute to delete rows by", ["artists", "album_name", "track_name", "popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature", "track_genre"])
                x = attribute_to_delete
                value_to_delete = st.text_input(f"Enter value for {attribute_to_delete} to delete rows", key="value_to_delete")
                delete_button = st.button("Submit", key="Delete_submit")
            if delete_button == True:
                if modify == "Delete Single Row":
                    # Validate the input
                    if not track_id_to_delete:
                        st.error("Track ID cannot be blank.")
                    else:
                        try:
                            # Determine which database to delete from based on the track_id hash
                            database_key = f"song_metadata_{hash_fun(track_id_to_delete)}"
                            audio_key = f"audio_elements_{hash_fun(track_id_to_delete)}"

                            collection = mongo_clients[database_key][database_key]["song"]
                            audio_collection = mongo_clients[audio_key][audio_key]["song"]
                            # Store track ID before deletion
                            deleted_track_ids = [track_id_to_delete]
                            # Delete the row
                            result = collection.delete_one({"_id": track_id_to_delete})
                            audio_result = audio_collection.delete_one({"_id": track_id_to_delete})
                            if result.deleted_count == 1 and audio_result.deleted_count == 1:
                                st.success(f"Deleted successfully into {database_key}!")
                                st.success(f"Deleted successfully into {audio_key}!")
                            else:
                                st.error("No matching row found to delete.")
                        except Exception as e:
                            st.error(f"An error occurred: {e}")
                
                if modify == "Delete Multiple Rows":
                    # Validate the input
                    if not value_to_delete:
                        st.error("Value cannot be blank.")
                    else:
                        try:
                            # Determine which database to delete from based on the attribute hash
                            if attribute_to_delete in ["artists", "album_name", "track_name", "track_genre"]:
                                database_keys = [f"song_metadata_{i}" for i in range(2)]
                                sister_database_keys = [f"audio_elements_{i}" for i in range(2)]

                            if attribute_to_delete in ["popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature"]:
                                print("attribute_to_delete second if:", attribute_to_delete)
                                value_to_delete = float(value_to_delete)
                                print("value_to_delete second if:", value_to_delete)
                                database_keys = [f"audio_elements_{i}" for i in range(2)]
                                sister_database_keys = [f"song_metadata_{i}" for i in range(2)]

                            for i in range(2):
                                collection = mongo_clients[database_keys[i]][database_keys[i]]["song"]
                                # Store track IDs before deletion
                                deleted_track_ids = [doc['_id'] for doc in collection.find({attribute_to_delete: value_to_delete})]
                                # Print deleted track IDs
                                print("Deleted Track IDs:", deleted_track_ids)
                                #delete rows from sister database
                                sister_collection = mongo_clients[sister_database_keys[i]][sister_database_keys[i]]["song"]
                                sister_result = sister_collection.delete_many({"_id": {"$in": deleted_track_ids}})
                                st.success(f"{sister_result.deleted_count} rows deleted successfully from {sister_database_keys[i]}!")
                                # Delete the rows from database
                                result = collection.delete_many({attribute_to_delete: value_to_delete})
                                st.success(f"{result.deleted_count} rows deleted successfully from {database_keys[i]}!")
                                
                            # for sister_database_key in sister_database_keys:
                            #     sister_collection = mongo_clients[sister_database_key][sister_database_key]["song"]
                            #     # Delete the rows
                            #     sister_result = sister_collection.delete_many({"_id": {"$in": deleted_track_ids}})
                            #     st.success(f"{sister_result.deleted_count} rows deleted successfully from {sister_database_key}!")
                                
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

    with st.sidebar:
        for i in range(15):
            st.text("")
        restart_button_clicked = st.button("Restart")
        if restart_button_clicked:
            st.session_state.submit_modifications_button_clicked = False
            st.session_state.submit_button_clicked = False
            st.session_state.insert_button_clicked = False
            st.session_state.modify_button_clicked = False
            st.session_state.entry1 = {}
            st.session_state.delete_button_clicked = False



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



if __name__ == "__main__":
    show_crud_operations()
