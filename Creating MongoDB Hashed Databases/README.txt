IMPORTANT NOTE: If you want to use Hashed_Databases.ipynb or Hashed_Databases.py, you need to change "mongodb_conn" to your own MongoDB ip address. The reason for this is because these files connect to Kyle Dinh's MongoDB server. If this file is run without changing "mongodb_conn", then an error will be produced because the data already exist in Kyle Dinh's MongoDB server on ec2. Please change "mongodb_conn" to your own MongoDB ip address.

One of the three documents is a csv file which contains the data we will be looking at. The dataset called "dataset.csv" comes from kaggle. The link is shown below:
https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset

This dataset has no missing values; however, it has many duplicate rows (over 40,0000 duplicate rows). These will be taken care of in the python files.

We decided to split the dataset into two datasets: song_metadata and audio_elements.

song_metadata contains the follwing attributes from the original dataset: 
	track_id, artists, album_name, track_name, track_genre

audio_elements contains the following attributes from the original dataset:
	"track_id", "popularity", "danceability", "energy", "key", "loudness",
        "mode", "speechiness", "acousticness", "instrumentalness", "liveness",
        "valence", "tempo", "time_signature"

We created two databases for each of the two datasets (four in total) based on a hash function. The hash function is used to hash "track_id".

Contained in this folder are Hashed_Databases.ipynb and Hashed_Databases.py. They do the same thing except one is a python notebook and the other is a python file.

These python files create the hashed datasets and adds the datasets to four mongodb databases based on the hash function. Read The first paragraph in this README before running either of the python files.

In order to run these programs, you also need to import two libraries: pandas and pymongo. If you do not have these libaries, then install them before using the files.

These python files will create four databases into MongoDB: song_metadata_0, song_metadata_1, audio_elements_0, audio_elements_1. Each of these four databases have a collection called "song". In MongoDB, the "track_id" is set to be equivalent to "_id".