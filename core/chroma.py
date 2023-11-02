#!/usr/bin/env python
# coding: utf-8

# All imports

import pickle
import pandas as pd
import os
import time
import warnings
import chromadb
import streamlit as st
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
warnings.filterwarnings("ignore")


# Create a ChromaDB
@st.cache_resource(show_spinner = False)
def create_or_get_chroma_db(chroma_file_path):

    # Writing chroma_file_path - Diagnostic
    # st.write(chroma_file_path)

    # Chroma will store its database files on disk, and load them on start
    db = chromadb.PersistentClient(path = chroma_file_path)

    # Create a client
    chroma_client = chromadb.EphemeralClient()

    # Get a collection object from an existing collection, by the name "quickstart". If it doesn't exist, create it.
    chroma_collection = db.get_or_create_collection("quickstart")

    # set up ChromaVectorStore and load in the collection object
    vector_store = ChromaVectorStore(chroma_collection = chroma_collection)

    # Set vector_store as a StorageContext attribute
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    return vector_store, storage_context


