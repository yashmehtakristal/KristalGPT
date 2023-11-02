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


def download_data_as_excel(orignal_excel_file):

    # buffer to use for excel writer
    buffer = io.BytesIO()

    # Open Excel file
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:

        # Write each dataframe to a different worksheet
        orignal_excel_file.to_excel(writer, sheet_name = "Final_Results", index = False)

        # Save writer
        writer.close()

        # Display download button for the dataframe
        st.download_button(label = "Download Output file as Excel File", data = buffer, file_name = "results.xlsx", mime = "application/vnd.ms-excel", key = "download_button", help = "Download your excel file", type="secondary", disabled = False, use_container_width = False)

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
