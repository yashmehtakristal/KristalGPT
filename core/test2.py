import streamlit as st
import tempfile
import os
import pandas as pd


# STACK OVERFLOW

def save_uploaded_file(uploadedfile):

    # Create the "tempDir" directory if it doesn't exist
    if not os.path.exists("tempDir"):
        os.makedirs("tempDir")
        
    with open(os.path.join("tempDir",uploadedfile.name).replace("\\","/"),"wb") as f:
        f.write(uploadedfile.getbuffer())
    
    return st.success("Saved file :{} in tempDir".format(uploadedfile.name))

datafile = st.file_uploader("Upload CSV",type=['csv'])

if datafile is not None:
    file_details = {"FileName":datafile.name,"FileType":datafile.type}
    df  = pd.read_csv(datafile)
    st.dataframe(df)
    # Apply Function here
    save_uploaded_file(datafile)


# SOMEONES GITHUB CODE

# file = st.file_uploader("File upload", type=["pdf"])

# with tempfile.NamedTemporaryFile(mode="wb") as temp:
#     bytes_data = file.getvalue()
#     temp.write(bytes_data)
#     print(temp.name)


# MY TESTS

# uploaded_files = st.file_uploader(
#     "Upload your pdf documents",
#     type=["pdf"],
#     help="You can upload multiple files."
#     "Please note that scanned documents are not supported yet!",
#     accept_multiple_files = True
# )

# # If accept_multiple_files = False, use this:
# # if uploaded_files:
# #    st.write("Filename: ", uploaded_files.name)

# # If accept_multiple_files = True, use this:
# if uploaded_files:
#    for uploaded_file in uploaded_files:
#        st.write("Filename: ", uploaded_file.name)


