DSCI-551-GROUP-PROJECT/
│
├── app.py               # Main application script to run the entire application
├── common_ui.py         # Common UI components (headers, sidebars)
├── mongo_utils.py       # MongoDB connection utilities
├── view.py              # Script for the "View Databases" functionality
├── modify.py            # Script for the "CRUD Operations" functionality
└── filter.py            # Script for the "Filter Data" functionality


Install:
pip install streamlit
pip install pymongo



To run:
streamlit run app.py

MongoClient("mongodb://Dsci-551:Dsci-551@3.18.103.247:27017/")
'mongodb://3.18.103.247:27017/'

def hash_fun(track_id): #hash function
    return sum(ord(c) for c in track_id) % 2
song_metadata_dbs = {
    0: "song_metadata_0",
    1: "song_metadata_1"
}

audio_elements_dbs = {
    0: "audio_elements_0",
    1: "audio_elements_1"
}

def hash_fun(track_id):
    return sum(ord(c) for c in track_id) % 2

# inserts the data into mongodb
def insert_data(row, db):
    # connect to MongoDB 
    client = MongoClient(mongodb_conn)
    
    # choose the database
    database = client[db]
    
    # choose the collection
    collection = database["song"]
    
    # insert data into the collection
    collection.insert_one(row)
    
    # close the connection
    client.close()