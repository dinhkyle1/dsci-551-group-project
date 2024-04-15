import streamlit as st
from common_ui import setup_sidebar, main_header, apply_dark_theme, apply_light_theme
from view import show_view_page
from modify import show_crud_operations
from filter import show_filter_page

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
        st.markdown("## Welcome to the Spotify Tracks Management System")
        st.markdown("Use the sidebar to navigate through different functionalities.")
    elif page == "View Databases":
        show_view_page()
    elif page == "CRUD Operations":
        show_crud_operations()
    elif page == "Filter Data":
        show_filter_page()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
# <<<<<<< HEAD

# =======
# >>>>>>> frontend
