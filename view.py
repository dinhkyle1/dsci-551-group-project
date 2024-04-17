import streamlit as st
from common_ui import apply_dark_theme, apply_light_theme
from mongo_utils import get_mongo_client
import pandas as pd

def show_view_page():
    # Apply theme based on the session state
    if st.session_state.get('theme', 'light') == 'dark':
        apply_dark_theme()
    else:
        apply_light_theme()

    # Apply custom styles to the select box
    custom_selectbox_style(st.session_state.get('theme', 'light'))  # This line calls your style function

    db_selection = st.selectbox("Select Database", ["Song Metadata", "Audio Elements"], key='db_select')
    mongo_clients = get_mongo_client()

    if db_selection == "Song Metadata":
        display_database(mongo_clients, "song_metadata_0")
        display_database(mongo_clients, "song_metadata_1")
    elif db_selection == "Audio Elements":
        display_database(mongo_clients, "audio_elements_0")
        display_database(mongo_clients, "audio_elements_1")

    # Close the MongoDB connections
    for client in mongo_clients.values():
        client.close()


def custom_selectbox_style(theme):
    # Define the background color for the dropdown based on the theme
    background_color = "#191414" if theme == 'dark' else "#FFFFFF"
    # Define the color for the text in the dropdown
    text_color = "#1DB954"  # Spotify green

    # Apply custom styles
    st.markdown(f"""
    <style>
        /* Style for the selectbox label using data-testid */
        label[data-testid="stWidgetLabel"] div {{
            color: {text_color} !important;
            font-weight: bold !important;
        }}

        /* Style for the selectbox itself and dropdown items */
        div[data-baseweb="select"] {{
            background-color: {background_color} !important;
            color: {text_color} !important;
        }}
        div[data-baseweb="select"] div[role="listbox"] ul {{
            background-color: {background_color} !important;
            color: {text_color} !important;
        }}
        div[data-baseweb="select"] div[role="listbox"] ul li {{
            background-color: {background_color} !important;
            color: {text_color} !important;
        }}
    </style>
    """, unsafe_allow_html=True)


def display_database(mongo_clients, db_key):
    """Displays data from the specified database in a table format with the correct theme."""
    client = mongo_clients[db_key]
    database = client[db_key]
    collection = database["song"]
    data = list(collection.find().limit(100))  # Displaying only the first 100 records

    if data:
        # Define colors for light and dark mode
        text_color = "#1DB954"  # Spotify green
        background_color = "#191414" if st.session_state.get('theme', 'light') == 'dark' else "#FFFFFF"
        border_color = "#191414" if st.session_state.get('theme', 'light') == 'dark' else "#dddddd"  # Match background or light gray

        # Styling for headers, borders, and the scrollable table
        st.markdown(f"<h2 style='color: {text_color};'>{db_key.replace('_', ' ').title()} Database</h2>", unsafe_allow_html=True)
        df = pd.DataFrame(data)
        df_html = df.to_html(index=False, escape=False)
        styled_df_html = (
            df_html.replace('<table border="1" class="dataframe">',
                            f'<table class="dataframe" style="width: 100%; border-collapse: collapse; border: 1px solid {border_color};">')
                  .replace('<thead>', f'<thead style="color: {text_color}; background-color: {background_color};">')
                  .replace('<tbody>', f'<tbody style="color: {text_color}; background-color: {background_color}; border: 1px solid {border_color};">')
        )

        # Scrollable div
        scrollable_table_style = f"""
        <div style='max-height:400px; overflow:auto;'>
            {styled_df_html}
        </div>
        """
        st.markdown(scrollable_table_style, unsafe_allow_html=True)

if __name__ == "__main__":
    show_view_page()
