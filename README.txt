I installed:
pip install streamlit
pip install pymongo

To run:
streamlit run dashboard.py

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