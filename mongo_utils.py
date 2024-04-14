from pymongo import MongoClient

def get_mongo_client():
    """ Returns a dictionary of MongoDB clients for each database. """
    database_urls = {
        "song_metadata_0": "mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/",
        "song_metadata_1": "mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/",
        "audio_elements_0": "mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/",
        "audio_elements_1": "mongodb://Dsci-551:Dsci-551@18.218.162.125:27017/"
    }
    
    # Create a MongoClient for each database URL and store them in a dictionary
    mongo_clients = {db: MongoClient(database_urls[db]) for db in database_urls}
    return mongo_clients
