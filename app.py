import streamlit as st
from common_ui import setup_sidebar, main_header, apply_dark_theme, apply_light_theme
from view import show_view_page
from modify import show_crud_operations
from filter import show_filter_page
from PIL import Image

# Initialize session state for the theme if it doesn't exist
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'light'

# Set the page config as the first command
st.set_page_config(page_title="Spotify Tracks Management", layout="wide")

def main():
    # Apply the theme at the start, based on the session state
    if st.session_state['theme'] == 'dark':
        apply_dark_theme()
    else:
        apply_light_theme()

    # Initialize the main header for the app
    main_header()

    # Setup sidebar and get the current page
    page = setup_sidebar("main_app_key")

    # Use the 'page' variable to determine which page to display
    if page == "Home":
        st.markdown("<h2 style='color: #1DB954;'>Welcome to the Spotify Tracks Management System</h2>", unsafe_allow_html=True)
        st.markdown("Use the sidebar to navigate through different functionalities.")
        for i in range(5):
            st.text("")
        st.markdown("*Our mission is to bridge the gap between data analysts, artists, and music lovers by leveraging advanced comprehensive database management to provide a deeper understanding of modern music trends through metadata insights . Through our user-friendly web application, we aim to empower artists with valuable insights into modern music trends, enabling them to refine their craft and connect with their audience more effectively. Additionally, we strive to provide music enthusiasts with personalized recommendations and a deeper understanding of their musical preferences. By facilitating seamless database analysis and modification, we aspire to enhance the music experience for all stakeholders involved.*")

    elif page == "View Databases":
        show_view_page()
    elif page == "CRUD Operations":
        show_crud_operations()
    elif page == "Filter Data":
        show_filter_page()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()

