DSCI-551-Group-Project/
│
├── app.py               # Main application script to run the entire application
├── common_ui.py         # Common UI components (headers, sidebars)
├── mongo_utils.py       # MongoDB connection utilities
├── view.py              # Script for the "View Databases" functionality
├── modify.py            # Script for the "CRUD Operations" functionality
└── filter.py            # Script for the "Filter Data" functionality

app.py: This is the main application script. It will import functions from view.py, modify.py, and filter.py 
to provide the functionality for each section for the Spotify Management System application.

common_ui.py: Contains UI functions that can be reused across all scripts; such as headers and sidebars.

mongo_utils.py: Manages MongoDB connections. This provides a function to connect to the databases, 
helps in avoiding repeated code across scripts that need database access.

view.py: Contains functions to view Spotify databases for userability.

modify.py: Contains userability functions of CRUD Operation such as insert, modify, delete data.

filter.py: Contains userability functions for filtering data by specific attributes. 


Set up environment: 
pip install streamlit
pip install pymongo
pip install --upgrade pillow

Run application:
streamlit run app.py

The CRUD Operations page offers a comprehensive toolkit tailored for data managers, facilitating seamless data manipulation within 
MongoDB databases. With functionalities encompassing Create, Read, Update, and Delete operations, data managers can efficiently 
handle database entries, ensuring data integrity and accessibility. Designed with data managers in mind, the page streamlines the 
process of interacting with database records, empowering users to insert, modify, or delete data with ease. However, its versatility 
extends beyond data managers, as it can be utilized by anyone seeking to interact with MongoDB databases for various purposes, 
including data analysis and exploration.

The Filter Data page caters to a broader audience, primarily targeting end users seeking simplified data exploration and analysis 
functionalities. With intuitive filtering options, users can effortlessly sift through datasets to extract relevant information 
based on their specific criteria. This user-friendly interface is crafted to accommodate individuals less familiar with database 
operations, offering a straightforward approach to data exploration without the need for extensive technical expertise. While the 
page is optimized for end users, its accessibility and ease of use make it suitable for anyone looking to interact with and derive 
insights from complex datasets, regardless of their level of technical proficiency.

Mongo Connection: 
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
