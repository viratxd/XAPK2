import os
import requests
import streamlit as st

def handle_file_upload(uploaded_file, upload_dir):
    input_path = os.path.join(upload_dir, uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    if " " in uploaded_file.name:
        new_name = uploaded_file.name.replace(" ", "_")
        new_input_path = os.path.join(upload_dir, new_name)
        if new_input_path != input_path:
            os.rename(input_path, new_input_path)
            input_path = new_input_path

    return input_path

def handle_url_download(url_input, upload_dir):
    st.write("Downloading APK from URL...")
    response = requests.get(url_input)
    if response.status_code == 200:
        input_path = os.path.join(upload_dir, os.path.basename(url_input))
        with open(input_path, "wb") as f:
            f.write(response.content)
        return input_path
    else:
        st.error("Failed to download APK from URL. Please check the URL and try again.")
        st.stop()