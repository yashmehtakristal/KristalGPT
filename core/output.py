#!/usr/bin/env python
# coding: utf-8

# All imports

import pickle
import pandas as pd
import os
import time
import warnings
import streamlit as st
import io
import base64 
import re
import uuid
warnings.filterwarnings("ignore")


def output_to_excel(orignal_excel_file, excel_directory, output_excel_filename, file_extension):
    '''
    output_to_excel: This function outputs the orignal_excel_file dataframe to an excel file

    Input - 
    orignal_excel_file: Dataframe of the results excel file
    excel_directory: Directory storing excel files
    output_excel_filename: Excel file name that we will output
    file_extension: Extension of the file that we wish output file will be 

    Output - None
    '''

    output_excel_file = f"{output_excel_filename}.{file_extension}"
    excel_file_path = os.path.join(excel_directory, output_excel_file)
    orignal_excel_file.to_excel(excel_file_path, index=True)


def download_data_as_excel_button(orignal_excel_file):

    # buffer to use for excel writer
    buffer = io.BytesIO()

    # Open Excel file
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:

        # Write each dataframe to a different worksheet
        orignal_excel_file.to_excel(writer, sheet_name = "Final_Results", index = False, header = True)

        # Save writer
        writer.close()

    # Generate a link to download the Excel file
    # st.download_button(label = "Download Output file as Excel File", data = buffer, file_name = "results.xlsx", mime = "application/vnd.ms-excel", key = "download_button", help = "Download your excel file", type="secondary", disabled = False, use_container_width = False)

    # st.markdown(
    #     f'<a href="data:application/vnd.ms-excel;base64,{buffer}" download="results.xlsx">Download Output file as Excel File</a>',
    #     unsafe_allow_html=True,
    # )

def download_data_as_excel_link(orignal_excel_file):

    # buffer to use for excel writer
    buffer = io.BytesIO()

    downloaded_file = orignal_excel_file.to_excel(buffer, index=False, header=True)

    buffer.seek(0)  # reset pointer

    b64 = base64.b64encode(buffer.read()).decode()  # some strings

    # Defining css attributes
    # button_uuid = str(uuid.uuid4()).replace('-', '')
    # button_id = re.sub('\d+', '', button_uuid)
    # custom_css = f""" 
    #     <style>
    #         #{button_id} {{
    #             display: inline-flex;
    #             align-items: center;
    #             justify-content: center;
    #             background-color: rgb(255, 255, 255);
    #             color: rgb(38, 39, 48);
    #             padding: .25rem .75rem;
    #             position: relative;
    #             text-decoration: none;
    #             border-radius: 4px;
    #             border-width: 1px;
    #             border-style: solid;
    #             border-color: rgb(230, 234, 241);
    #             border-image: initial;
    #         }} 
    #         #{button_id}:hover {{
    #             border-color: rgb(246, 51, 102);
    #             color: rgb(246, 51, 102);
    #         }}
    #         #{button_id}:active {{
    #             box-shadow: none;
    #             background-color: rgb(246, 51, 102);
    #             color: white;
    #             }}
    #     </style> """

    # link = custom_css + f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="results.xlsx">Download excel file</a>'
    link = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="results.xlsx">Download excel file</a>'

    st.markdown(link, unsafe_allow_html=True)



@st.cache_data
def convert_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


def download_data_as_csv(orignal_excel_file):

    # Call above function convert_to_csv
    csv = convert_to_csv(df = orignal_excel_file)

    # download button 1 to download dataframe as csv
    st.download_button(
        label = "Download Output file as CSV File",
        data = csv,
        file_name = 'results.csv',
        mime= 'text/csv'
    )


def download_data_as_csv_link(orignal_excel_file):

    # Call above function convert_to_csv
    csv = orignal_excel_file.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()

    # Defining css style
    # button_uuid = str(uuid.uuid4()).replace('-', '')
    # button_id = re.sub('\d+', '', button_uuid)
    # custom_css = f""" 
    #     <style>
    #         #{button_id} {{
    #             display: inline-flex;
    #             align-items: center;
    #             justify-content: center;
    #             background-color: rgb(255, 255, 255);
    #             color: rgb(38, 39, 48);
    #             padding: .25rem .75rem;
    #             position: relative;
    #             text-decoration: none;
    #             border-radius: 4px;
    #             border-width: 1px;
    #             border-style: solid;
    #             border-color: rgb(230, 234, 241);
    #             border-image: initial;
    #         }} 
    #         #{button_id}:hover {{
    #             border-color: rgb(246, 51, 102);
    #             color: rgb(246, 51, 102);
    #         }}
    #         #{button_id}:active {{
    #             box-shadow: none;
    #             background-color: rgb(246, 51, 102);
    #             color: white;
    #             }}
    #     </style> """

    # Generate a link to download the Excel file
    # link = custom_css + f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download csv file</a>'
    link = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download csv file</a>'
    st.markdown(link, unsafe_allow_html=True)


def download_data_as_excel_old(orignal_excel_file):

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    excel_writer = pd.ExcelWriter("results.xlsx", engine="xlsxwriter")

    # Convert the DataFrame to an XlsxWriter Excel object.
    orignal_excel_file.to_excel(excel_writer, sheet_name = "Final_Results", index = False)

    # Close the Pandas Excel writer and output the Excel file.
    excel_writer.save()

    with open("results.xlsx", "rb") as f:
        data = f.read()
    
    return data
