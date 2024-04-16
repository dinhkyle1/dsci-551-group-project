## imports the spotify dataset to Kyle Dinh's ec2 instance 

## if you want to import the dataset to your own ec2 instance:
##    1.) download the spotify csv file "dataset.csv" and make sure its in the working directory
##    2.) change mongodb_conn below to your own mongodb ip address
##    3.) make sure permissions are set so you can access mongodb from your device

import pandas as pd
from pymongo import MongoClient

# importing the data
spotify_data = pd.read_csv("dataset.csv")

song_metadata_cols = ["track_id", "artists", "album_name", "track_name", "track_genre"]
audio_elements_cols = ["track_id", "popularity", "danceability", "energy", "key", "loudness",
                       "mode", "speechiness", "acousticness", "instrumentalness", "liveness",
                       "valence", "tempo", "time_signature"]

### use your own mongodb ip address!! ###
mongodb_conn = 'mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/'

hash_vals = []

# selects specific columns 
song_metadata = spotify_data[song_metadata_cols]
audio_elements = spotify_data[audio_elements_cols]

# renames "track_id" to "_id" for mongodb
song_metadata = song_metadata.rename(columns = {"track_id": "_id"})
audio_elements = audio_elements.rename(columns = {"track_id": "_id"})

# removes duplicate rows in the dataframe
song_metadata = song_metadata.drop_duplicates(subset = ["_id"], ignore_index = True)
audio_elements = audio_elements.drop_duplicates(subset = ["_id"], ignore_index = True)

# mongodb databases
song_metadata_dbs = {
    0: "song_metadata_0",
    1: "song_metadata_1"
}

audio_elements_dbs = {
    0: "audio_elements_0",
    1: "audio_elements_1"
}

# hash sum of the ascii characters in track_id
def hash_fun(track_id):
    return sum(ord(c) for c in track_id) % 2

# inserts the data into mongodb
def insert_data(data, db):
    # connect to MongoDB 
    client = MongoClient(mongodb_conn)
    
    # choose the database
    database = client[db]
    
    # choose the collection
    collection = database["song"]
    
    # insert data into the collection
    collection.insert_many(data)
    
    # close the connection
    client.close()

if __name__ == "__main__":
    # the hash value for each row of the two dataframes are the same
    for row_index in range(song_metadata.shape[0]):
        song_metadata_row = song_metadata.iloc[row_index,:]
    
        hash = hash_fun(song_metadata_row.iloc[0])
        
        if hash == 0:
            hash_vals.append(0)
        else:
            hash_vals.append(1)
    
    # adds a column called hash for each dataframe
    song_metadata["hash"] = hash_vals
    audio_elements["hash"] = hash_vals
    
    # creates new datframes based on the hash value
    song_metadata_0 = song_metadata[song_metadata["hash"] == 0]
    song_metadata_1 = song_metadata[song_metadata["hash"] == 1]
    audio_elements_0 = audio_elements[audio_elements["hash"] == 0]
    audio_elements_1 = audio_elements[audio_elements["hash"] == 1]
    
    # removes the hash column
    song_metadata_0 = song_metadata_0.iloc[:,:-1]
    song_metadata_1 = song_metadata_1.iloc[:,:-1]
    audio_elements_0 = audio_elements_0.iloc[:,:-1]
    audio_elements_1 = audio_elements_1.iloc[:,:-1]
    
    # resets index of each dataframe
    song_metadata_0 = song_metadata_0.reset_index(drop = True)
    song_metadata_1 = song_metadata_1.reset_index(drop = True)
    audio_elements_0 = audio_elements_0.reset_index(drop = True)
    audio_elements_1 = audio_elements_1.reset_index(drop = True)
    
    # adds the data to each database based on the hash
    insert_data(song_metadata_0.to_dict(orient = "records"), song_metadata_dbs[0])
    insert_data(song_metadata_1.to_dict(orient = "records"), song_metadata_dbs[1])
    insert_data(audio_elements_0.to_dict(orient = "records"), audio_elements_dbs[0])
    insert_data(audio_elements_1.to_dict(orient = "records"), audio_elements_dbs[1])
