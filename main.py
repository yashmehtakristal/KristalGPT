# All imports

import streamlit as st

# Setting page config & header
st.set_page_config(page_title="KristalGPT", page_icon="📖", layout="wide", initial_sidebar_state="expanded")
st.header("📖 Kristal GPT")

import openai
import os
import tempfile
from tempfile import NamedTemporaryFile
import tkinter as tk
from tkinter import filedialog
from streamlit_extras.app_logo import add_logo
from st_pages import Page, Section, add_page_title, show_pages, hide_pages
from database_helper_functions import sign_up, fetch_users
import streamlit_authenticator as stauth

## Importing functions

# from ui import (
#     is_query_valid,
#     display_file_read_error,
# )

# from bundle import no_embeddings_process_documents, embeddings_process_documents
# from core.loading import read_documents_from_directory, iterate_files_from_directory, save_uploaded_file, read_documents_from_uploaded_files, get_tables_from_uploaded_file, iterate_files_from_uploaded_files, iterate_excel_files_from_directory, iterate_uploaded_excel_files, print_file_details, show_dataframes, iterate_uploaded_excel_file
# from core.pickle import save_to_pickle, load_from_pickle
# from core.indexing import query_engine_function, build_vector_index
# from core.LLM_preprocessing import conditions_excel, extract_fund_variable, prompts_to_substitute_variable, storing_input_prompt_in_list
# from core.querying import recursive_retriever_old, recursive_retriever
# from core.LLM_prompting import individual_prompt, prompt_loop
# from core.PostLLM_prompting import create_output_result_column, create_output_context_column, intermediate_output_to_excel
# from core.parsing import create_schema_from_excel, parse_value
# from core.Postparsing import create_filtered_excel_file, final_result_orignal_excel_file, reordering_columns
# from core.Last_fixing_fields import find_result_fund_name, find_result_fund_house, find_result_fund_class, find_result_currency, find_result_acc_or_inc, create_new_kristal_alias, update_kristal_alias, update_sponsored_by, update_required_broker, update_transactional_fund, update_disclaimer, update_risk_disclaimer, find_nav_value, update_nav_value 
# from core.output import output_to_excel, download_data_as_excel, download_data_as_csv

# Add the logo to the sidebar
add_logo("https://assets-global.website-files.com/614a9edd8139f5def3897a73/61960dbb839ce5fefe853138_Kristal%20Logotype%20Primary.svg")

show_pages(
    [
        Page("main.py","Sign Up/Login", "🗝️"),
        Page("pages/home.py", "Home", "🏠"),
        # Section(name = "Bulk Upload", icon="📚"),
        Page("pages/bulk_upload_basic.py", "Bulk Upload - Basic", "📚"),
        Page("pages/bulk_upload_advanced.py", "Bulk Upload - Advanced", "📚"),
        # Section(name = "QA Basic", icon="❓"),
        Page("pages/qa_basic.py", "Q&A - Basic", "❓"),
        Page("pages/qa_advanced.py", "Q&A - Advanced", "❓"),
        # Section(name = "Chatbot", icon="💬"),
        # Page("pages/chatbot_without_memory.py", "Chatbot - Basic", "💬"),
        # Page("pages/chatbot_with_memory.py", "Chatbot - Advanced", "💬")
    ]
)

# Session state variable to save "logged out" boolean value
if "logged_out" not in st.session_state:
    st.session_state.logged_out = False

# Session state variable to save "logged in" boolean value
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Hide particular pages if not logged in
if not st.session_state.logged_in:
    hide_pages(["Home", "Bulk Upload - Basic", "Bulk Upload - Advanced", "Q&A - Basic", "Q&A - Advanced"])

# Hide particular pages if logged out
if st.session_state.logged_out:
    hide_pages(["Home", "Bulk Upload - Basic", "Bulk Upload - Advanced", "Q&A - Basic", "Q&A - Advanced"])


# Session state variable to save "username"
if "username" not in st.session_state:
    st.session_state.username = ''

# Session state variable to save "Authenticator" object
if "Authenticator" not in st.session_state:
    st.session_state.Authenticator = None

# Session state variable to save "Logout" object
if "logout" not in st.session_state:
    st.session_state.logout = False


try:
    # Calling the fetch_users() function which returns a dictionary of users
    users = fetch_users()

    # Will store the respective keys in the dictionary in the following lists
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    # Storing the credentials for each user in a dictionary
    credentials = {'usernames': {}}
    
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    # Now credentials will look like this (need to format it like that for stauth.Authenticate to accept it):
    # credentials = {'usernames: {'username_from_list': 'emails_from_list', 'password_from_list'}}

    # Create an authentication object of the credentials
    # Along, with the name of the cookie (to reauthenticate user without them re-entering credentials, so they can refresh page without providing their password again)
    # Write random key to hash a cookies signature (abcdef)
    # Specify number of days cookie can be used for (30 days)
    Authenticator = stauth.Authenticate(credentials, cookie_name = 'Streamlit', key = 'abcdef', cookie_expiry_days = 30)

    # Save Authenticator to session state
    st.session_state.Authenticator = Authenticator

    # Get the email, authentication status and username from Login module
    email, authentication_status, username = Authenticator.login('Login', 'main')

    info, info1 = st.columns(2)

    # If the provided email, username and password does not match authentication, display the signup module
    if not authentication_status:
        sign_up()

    # st.write(usernames)

    # If username is provided
    if username:

        # If username in the usernames list (from database)
        if username in usernames:

            # Save the username to session state
            st.session_state.username = username

            # If authentication status is True
            if authentication_status:

                # Setting session state of logged in = True
                # & log out = False
                st.session_state.logged_in = True
                st.session_state.logout = False

                # let User see app
                st.sidebar.subheader(f'Welcome {username}')
                logout_button = Authenticator.logout('Log Out', 'sidebar')

                # If user has clicked logged_out button, update the state variables
                if logout_button:
                    st.session_state.logged_out = True
                    st.session_state.logged_in = False


                # Show the rest of the pages 
                # show_pages(
                #     [
                #         Page("pages/home.py", "Home", "🏠"),
                #         # Section(name = "Bulk Upload", icon="📚"),
                #         Page("pages/bulk_upload_basic.py", "Bulk Upload - Basic", "📚"),
                #         Page("pages/bulk_upload_advanced.py", "Bulk Upload - Advanced", "📚"),
                #         # Section(name = "QA Basic", icon="❓"),
                #         Page("pages/qa_basic.py", "Q&A - Basic", "❓"),
                #         Page("pages/qa_advanced.py", "Q&A - Advanced", "❓"),
                #         # Section(name = "Chatbot", icon="💬"),
                #         # Page("pages/chatbot_without_memory.py", "Chatbot - Basic", "💬"),
                #         # Page("pages/chatbot_with_memory.py", "Chatbot - Advanced", "💬")
                #     ]
                # )

        # ERROR HANDLING
            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            
            else:
                with info:
                    st.warning('Please feed in your credentials')
        
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')


except:
    st.success('Refresh Page')

