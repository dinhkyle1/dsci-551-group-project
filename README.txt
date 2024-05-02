DSCI-551-Group-Project/
│
├── app.py               # Main application script to run the entire application
├── common_ui.py         # Common UI components (headers, sidebars)
├── mongo_utils.py       # MongoDB connection utilities
├── view.py              # Script for the "View Databases" functionality for Users
├── modify.py            # Script for the "CRUD Operations" functionality for Data Managers
└── filter.py            # Script for the "Filter Data" functionality for Users

app.py: This is the main application script. It will import functions from view.py, modify.py, and filter.py 
to provide the functionality for each section for the Spotify Management System application.

common_ui.py: Contains UI functions that can be reused across all scripts; such as headers and sidebars.

mongo_utils.py: Manages MongoDB connections. This provides a function to connect to the databases, 
helps in avoiding repeated code across scripts that need database access.

view.py: Contains functions to view Spotify databases for userability.

modify.py: Contains data manager functions of CRUD Operation such as insert, modify, delete data.

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
