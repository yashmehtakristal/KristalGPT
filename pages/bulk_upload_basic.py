# All imports

import streamlit as st
from streamlit_extras.app_logo import add_logo
from st_pages import Page, Section, add_page_title, show_pages, hide_pages

# Setting page config & header
st.set_page_config(page_title = "Kristal Retriever", page_icon = "📖", layout = "wide")
st.header("📖 Kristal Retriever")

# Hide particular pages if not logged in
if not st.session_state.logged_in:
    hide_pages(["Bulk Upload - Basic", "Bulk Upload - Advanced", "Q&A - Basic", "Q&A - Advanced"])

# Hide particular pages if logged out
if st.session_state.logged_out:
    hide_pages(["Bulk Upload - Basic", "Bulk Upload - Advanced", "Q&A - Basic", "Q&A - Advanced"])

add_logo("https://assets-global.website-files.com/614a9edd8139f5def3897a73/61960dbb839ce5fefe853138_Kristal%20Logotype%20Primary.svg")

import openai
import os
import tempfile
from tempfile import NamedTemporaryFile
import zipfile


## Importing functions

from ui import (
    is_query_valid,
    display_file_read_error,
)

from bundle import no_embeddings_process_documents_loop, embeddings_process_documents_loop
from core.chroma import st_server_file, print_files_in_particular_directory, upload_zip_files, print_files_in_directory, check_zipfile_directory

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


### CODE

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY
openai_api_key = OPENAI_API_KEY

# Error handling for OpenAI API key
if not openai_api_key:
    st.warning(
        "There is something wrong with the API Key Configuration."
        "Please check with creator of the program (OpenAI keys can be found at https://platform.openai.com/account/api-keys)"
    )


# Display app only if user is logged in
if st.session_state.logged_in is True and st.session_state.logout is False:

    st.sidebar.subheader(f'Welcome {st.session_state.username}')

    logout_button = st.session_state.Authenticator.logout('Log Out', 'sidebar')

    # If user has clicked logged_out button, update the state variables
    if logout_button:
        st.session_state.logged_out = True
        st.session_state.logged_in = False
        st.rerun()


    # Check embeddings
    check_embeddings = st.radio(label = "Do you have saved embeddings?", options = ["Yes", "No"], index = None, help = "Embeddings are saved files created by ChromaDB", disabled=False, horizontal = False, label_visibility="visible")


    # User does not have embeddings they can use
    if check_embeddings == "No":

        # Obtain chrome_file_path and chroma_file_name
        master_folder, chroma_file_path, chroma_file_name = st_server_file()

        # print_files_in_particular_directory(master_folder)
        # print_files_in_particular_directory(chroma_file_path)

        # File uploader section for pdfs
        uploaded_files = st.file_uploader(
        "Upload your pdf documents",
        type=["pdf"],
        help="You can upload multiple files."
        "Please note that scanned documents are not supported yet!",
        accept_multiple_files = True
    )

        # File uploader section for xlsx
        uploaded_xlsx_files = st.file_uploader(
        "Upload a xlsx file",
        type=["xlsx"],
        help="Please upload the excel file. Make sure it is in the appropriate format. Check the [name] sidebar for more details about the format",
        accept_multiple_files = False
    )
        
        # Fund name variable
        fund_variable = st.text_input(
            label = "Fund name:",
            value = None,
            max_chars = None,
            type = "default",
            help = "This will be used to replace the word, fund, in certain prompts",
            placeholder = '''Please input the exact, full fund name. Example: FRANKLIN US GOVERNMENT "A" INC''',
            disabled = False,
            label_visibility = "visible"
        )
        
        

    # User has embeddings which they can use
    elif check_embeddings == "Yes":
        
        uploaded_zip_file = upload_zip_files()

        # print_files_in_directory(chroma_file_path)

        # File uploader section for pdfs
        uploaded_files = st.file_uploader(
        "Upload your pdf documents",
        type=["pdf"],
        help="You can upload multiple files."
        "Please note that scanned documents are not supported yet!",
        accept_multiple_files = True
    )

        # File uploader section for xlsx
        uploaded_xlsx_files = st.file_uploader(
        "Upload a xlsx file",
        type=["xlsx"],
        help="Please upload the excel file. Make sure it is in the appropriate format. Check the [name] sidebar for more details about the format",
        accept_multiple_files = False)

        # Fund name variable
        fund_variable = st.text_input(
            label = "Fund name:",
            value = None,
            max_chars = None,
            type = "default",
            help = "This will be used to replace the word, fund, in certain prompts",
            placeholder = '''Please input the exact, full fund name. Example: FRANKLIN US GOVERNMENT "A" INC''',
            disabled = False,
            label_visibility = "visible"
        )

    # No value inserted for check_embeddings - raise warning
    else:
        st.warning("Please select whether you have embeddings to use or not")
        st.stop()


    # If user clicks on the button process
    if st.button("Process documents", type = "primary"):

        # User does not have embeddings they can use
        if check_embeddings == "No":
            
            # Checking if both conditions are satisfied
            if uploaded_files and uploaded_xlsx_files:
                    
                # Call bundle function - no_embeddings_process_documents
                no_embeddings_process_documents_loop(uploaded_files = uploaded_files, uploaded_xlsx_files = uploaded_xlsx_files, chroma_file_path = chroma_file_path, fund_variable = fund_variable)

                # Printing files in particular directory
                # print_files_in_particular_directory(chroma_file_path)


            ## ERROR HANDLING FOR ALL 2 FILE UPLOADS

            ## 1 CONDITION NOT SATISFIED

            elif uploaded_files and not uploaded_xlsx_files:
                st.warning("1) Please upload an excel file", icon="⚠")
                st.stop()


            elif uploaded_xlsx_files and not uploaded_files:
                st.warning("1) Please upload pdf files", icon="⚠")
                st.stop()

            # ALL 2 CONDITIONS NOT SATISFIED
            else:
                st.warning(
                    '''
                    1) Please upload the pdf files
                    2) and upload the excel files''',
                    icon="⚠")
                st.stop()


        # User does not have embeddings they can use
        elif check_embeddings == "Yes":

            # Checking if all three conditions are satisfied
            if uploaded_files and uploaded_xlsx_files:

                # Call bundle function - no_embeddings_process_documents
                embeddings_process_documents_loop(uploaded_files = uploaded_files, uploaded_xlsx_files = uploaded_xlsx_files, fund_variable = fund_variable, uploaded_zip_file = uploaded_zip_file)

            ## ERROR HANDLING FOR ALL 2 FILE UPLOADS

            ## 1 CONDITION NOT SATISFIED

            elif uploaded_files and not uploaded_xlsx_files:
                st.warning("1) Please upload an excel file", icon="⚠")
                st.stop()


            elif uploaded_xlsx_files and not uploaded_files:
                st.warning("1) Please upload pdf files", icon="⚠")
                st.stop()

            # ALL 2 CONDITIONS NOT SATISFIED
            else:
                st.warning(
                    '''
                    1) Please upload the pdf files
                    2) and upload the excel files''',
                    icon="⚠")
                st.stop()


else:
    st.info("Seems like you are not logged in. Please head over to the Login page to login", icon="ℹ️")