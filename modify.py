import streamlit as st
from common_ui import main_header
from mongo_utils import get_mongo_client

def show_crud_operations():
    #main_header()
    if st.button("Insert Record", key='insert_record'):
        # Toggle the display of the insert form
        st.session_state.show_insert_form = not st.session_state.get("show_insert_form", False)

    if st.session_state.get("show_insert_form", False):
        with st.form(key='insert_form'):
            st.write("### Insert New Record")
            entry = {
                # ... all the form fields ...
            }
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # Insert the entry into the database
                insert_record(entry)

def insert_record(entry):
    mongo_clients = get_mongo_client()
    try:
        # Hash function to decide which database to use
        db_key = f"song_metadata_{hash_fun(entry['track_id'])}"
        db = mongo_clients[db_key]
        collection = db['song']
        collection.insert_one(entry)
        st.success("Record inserted successfully!")
    except Exception as e:
        st.error(f"Error inserting record: {str(e)}")
    finally:
        for client in mongo_clients.values():
            client.close()

def hash_fun(track_id):
    # Hash function logic
    pass

if __name__ == "__main__":
    show_crud_operations()

