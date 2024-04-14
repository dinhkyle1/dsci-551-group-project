import streamlit as st

def main_header():
    """ Renders the main header for the application. """
    st.markdown("""
        <h1 style='text-align: center; color: var(--primary-color);'>Spotify Tracks Management System</h1>
        <hr style='height: 2px; background-color: var(--primary-color);'>
        """, unsafe_allow_html=True)

def dark_theme_css():
    """ Returns the CSS for the dark theme. """
    return '''
        <style>
            :root {
                --primary-color: #1DB954;
                --background-color: #191414;
                --text-color: #1DB954;
            }
            body, .stApp, .stTextInput > input, .stSelectbox > select, .stTextArea > textarea,
            .stButton > button, .st-bb, .st-br {
                background-color: var(--background-color);
                color: var(--text-color);
            }
            .stSidebar > div, .st-sb {
                background-color: var(--background-color);
            }
            .css-1yjuwjr, .st-bd {
                color: var(--text-color);
            }
            .stButton > button {
                border: 1px solid var(--text-color);
            }
            /* Additional styling rules for other elements as needed */
        </style>
    '''

def light_theme_css():
    """ Returns the CSS for the light theme. """
    return '''
        <style>
            :root {
                --primary-color: #1DB954;
                --background-color: #FFFFFF;
                --text-color: #1DB954;
            }
            body, .stApp {
                background-color: var(--background-color) !important;
                color: var(--primary-color)!important; 
            }
            .stTextInput > input, .stSelectbox > select, .stTextArea > textarea, .stTextInput label, .stSelectbox label, .stTextArea label {
                background-color: var(--background-color) !important;
                color: var(--text-color) !important;
                border-color: var(--text-color) !important;
            }
            .stButton > button {
                background-color: var(--background-color) !important;
                color: var(--primary-color) !important;
                border-color: var(--primary-color) !important;
            }
            .stCheckbox > div, .stRadio > label, .stSlider > div, .stSlider label, .css-j7qwjs {
                background-color: var(--background-color) !important;
                color: var(--primary-color) !important;
            }
            .stSidebar > div {
                background-color: var(--background-color) !important;
            }
            .css-1yjuwjr {
                color: var(--primary-color) !important;
            }
            /* Add other selectors and rules for light theme styling as needed */
            /* Specific styles for the search query label and input */
            div[data-baseweb="input"] > div {
                background-color: var(--background-color) !important;
                color: var(--text-color) !important;
            }
            label[data-baseweb="form-control"] .css-1nrlq1o {
                color: var(--text-color) !important;
            }
            /* Ensure proper visibility of the placeholder text */
            ::placeholder {
                color: var(--text-color) !important;
                opacity: 0.5;
            }
        </style>
    '''


def setup_sidebar(unique_key):
    """ Sets up the sidebar for navigation and theme toggling. """
    st.sidebar.title('Navigation')
    theme = st.sidebar.checkbox("Toggle Dark Mode", value=False, key='toggle_theme', on_change=toggle_theme)
    if theme:
        apply_dark_theme()
    else:
        apply_light_theme()
    
    page = st.sidebar.radio(
        "Go to",
        ["Home", "View Databases", "CRUD Operations", "Filter Data"],
        key=unique_key
    )
    return page

def toggle_theme():
    """Toggle the theme state in the session."""
    st.session_state['theme'] = 'dark' if st.session_state['toggle_theme'] else 'light'


def apply_dark_theme():
    """ Applies the dark theme CSS. """
    st.markdown(dark_theme_css(), unsafe_allow_html=True)

def apply_light_theme():
    """ Applies the light theme CSS. """
    st.markdown(light_theme_css(), unsafe_allow_html=True)


