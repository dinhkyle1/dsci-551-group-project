U
    }�f�  �                   @   sD   d dl Zdd� Zdd� Zdd� Zdd	� Zd
d� Zdd� Zdd� ZdS )�    Nc                   C   s   t jddd� dS )z. Renders the main header for the application. z�
        <h1 style='text-align: center; color: var(--primary-color);'>Spotify Tracks Management System</h1>
        <hr style='height: 2px; background-color: var(--primary-color);'>
        T��unsafe_allow_htmlN)�st�markdown� r   r   �;/Users/Aj/final project/dsci-551-group-project/common_ui.py�main_header   s    �r   c                   C   s   dS )z% Returns the CSS for the dark theme. a@  
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
    r   r   r   r   r   �dark_theme_css
   s    r	   c                   C   s   dS )z& Returns the CSS for the light theme. a�  
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
    r   r   r   r   r   �light_theme_css%   s    r
   c                 C   sP   t j�d� t jjdddtd�}|r,t�  nt�  t jjdddd	d
g| d�}|S )z8 Sets up the sidebar for navigation and theme toggling. Z
NavigationzToggle Dark ModeF�toggle_theme)�value�key�	on_changezGo to�HomezView DatabaseszCRUD OperationszFilter Data)r   )r   �sidebar�title�checkboxr   �apply_dark_theme�apply_light_theme�radio)Z
unique_key�theme�pager   r   r   �setup_sidebarX   s    
�r   c                   C   s   t jd rdndt jd< dS )z&Toggle the theme state in the session.r   �dark�lightr   N)r   �session_stater   r   r   r   r   h   s    r   c                   C   s   t jt� dd� dS )z Applies the dark theme CSS. Tr   N)r   r   r	   r   r   r   r   r   m   s    r   c                   C   s   t jt� dd� dS )z Applies the light theme CSS. Tr   N)r   r   r
   r   r   r   r   r   q   s    r   )	�	streamlitr   r   r	   r
   r   r   r   r   r   r   r   r   �<module>   s   3