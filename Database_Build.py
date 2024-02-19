#!/usr/bin/env python
# coding: utf-8

# ## Song Metadata DB 
# 
# #### Found Here: https://song-metadata-default-rtdb.firebaseio.com/
# 
# Purpose: To store basic information about each track, useful for general queries and indexing.
# 
# Columns / Variables : track_id, artists, album_name, track_name, popularity, duration_ms, explicit, track_genre.
# 
#  
# 
# ##  Audio Elements DB
# 
# #### Found Here: https://audio-elements-e5904-default-rtdb.firebaseio.com/
# 
# Purpose: To store detailed audio features of each song, useful for analysis and recommendation algorithms.
# 
# Columns/ Variables : track_id, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature.

# In[2]:


#requirements
pip install firebase-admin


# In[1]:


#Import Libraries/Modules
import os
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db


# In[2]:


#Load data
file_path = 'spotify_data.csv'
spotify_data = pd.read_csv(file_path)

#Split the data into two DF's
song_metadata_cols = ['track_id', 'artists', 'album_name', 'track_name', 'track_genre']
audio_elements_cols = ['track_id', 'popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']

#Assign new Df's
song_metadata = spotify_data[song_metadata_cols]
audio_elements = spotify_data[audio_elements_cols]


# ## Instructions to find or generate the JSON Firebase DB Key file:
# 
# 1. Go to the Firebase Console: Visit Firebase Console and select your project.
# 
# 2. Access Project Settings: Click on the gear icon next to "Project Overview" in the sidebar and select "Project settings."
# 
# 3. Navigate to Service Accounts: In the project settings, go to the "Service accounts" tab.
# 
# 4. Generate a New Private Key: Click on the "Generate new private key" button. A JSON file will be downloaded to your computer.
# 
# 5. The path you need to provide in the script is the location where this JSON file is saved

# ## On macOS or Linux, use the export command in the terminal: 
# 
# 
# ### Option 1:
# export SONG_METADATA_CREDENTIALS=path/to/song_metadata_credentials.json
# 
# export AUDIO_ELEMENTS_CREDENTIALS=path/to/audio_elements_credentials.json
# 
# ### Option 2:
# 
# Set the os variabels directly in the environment using  'os.environ'.  Replace path\to\song_metadata_credentials.json and path\to\audio_elements_credentials.json with the actual paths to your own credentials files.
# 
# Each collaborator can set these environment variables on their own machine, ensuring that sensitive information is kept secure and out of version control.
# 
# 

# In[5]:


os.environ['SONG_METADATA_CREDENTIALS'] = 'YOUR PATH TO firebases JSON SONG-METADATA.json'

os.environ['AUDIO_ELEMENTS_CREDENTIALS'] = 'YOUR PATH TO firebases JSON AUDIO-ELEMENTS.json'


# In[6]:


#Initialize Firebase Admin SDK for both databases using environment variables
cred_song_metadata = credentials.Certificate(os.environ.get('SONG_METADATA_CREDENTIALS'))
firebase_admin.initialize_app(cred_song_metadata, {
    'databaseURL': 'https://song-metadata-default-rtdb.firebaseio.com/'
}, name='song_metadata')

cred_audio_elements = credentials.Certificate(os.environ.get('AUDIO_ELEMENTS_CREDENTIALS'))
firebase_admin.initialize_app(cred_audio_elements, {
    'databaseURL': 'https://audio-elements-e5904-default-rtdb.firebaseio.com/'
}, name='audio_elements')


# In[11]:


def upload_data_to_firebase(df, db_url, db_name):
    ref = db.reference('/', app=firebase_admin.get_app(db_name))
    for index, row in df.iterrows():
        #convert the row to a dictionary and replace NaN and infinite values
        row_dict = row.to_dict()
        for key, value in row_dict.items():
            if pd.isna(value) or value in [float('inf'), float('-inf')]:
                row_dict[key] = None  # replace with None or a suitable value

        #check if the record already exists, so we do not upload duplicate songs
        track_id = str(row['track_id'])
        if ref.child(track_id).get() is None:
            ref.child(track_id).set(row_dict)
        else:
            print(f"Skipping existing record: {track_id}")


# In[12]:


#Upload song metadata to Firebase 
upload_data_to_firebase(song_metadata, 'https://song-metadata-default-rtdb.firebaseio.com/', 'song_metadata')


# In[10]:


# Upload audio elements to Firebase
upload_data_to_firebase(audio_elements, 'https://audio-elements-e5904-default-rtdb.firebaseio.com/', 'audio_elements')


# ### The END! 
