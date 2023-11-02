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



# File uploader used to select directory from embedding
embedding_upload = st.file_uploader(
    "Please select a particular directory",
    type=["txt"],
    help="Please use this file uploader, primarily to choose a particular directory to save your embeddings to. Would recommend creating a sample.txt in the corresponding folder",
    accept_multiple_files = False
)

if embedding_upload:

    # Working Code for getting file path in a temporary directory in C:\Users\user\AppData\Local\Temp\

    temp_dir = tempfile.mkdtemp()
    chroma_file_path = os.path.join(temp_dir, embedding_upload.name)
    st.write(chroma_file_path)

    # Working Code for getting file path in same directory

    # with NamedTemporaryFile(dir='.', suffix='.txt') as f:

    #     # Saving file path where chroma will be stored
    #     chroma_file_path = f.name
        
    #     # Write the file path for Diagnostic purposes
    #     st.write(chroma_file_path)

if not embedding_upload:
    st.warning("Please select a particular directory (needed to save embeddings)", icon="⚠")
    st.stop()






### NEXT CODE SNIPPET


    # User did not click on Folder Picker button
    else:
        st.warning("Please enter directory which will be used to load embeddings")
        st.stop()
