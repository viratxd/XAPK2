import streamlit as st
import os
from utils.apk_debug import debug_apk
from utils.apk_process import process_xapk, process_sign, xapk_debug
from utils.file_handling import handle_file_upload, handle_url_download
from utils.cleanup import cleanup_files

st.title("APK File Processor")

uploaded_file = st.file_uploader("Upload APK file", type=['apk', 'xapk', 'apks'])
url_input = st.text_input("Or enter APK URL")
processing_option = st.radio("Choose the processing type:", ('Process XAPK', 'Sign APK', 'Debug APK', 'XAPK Debug'))

if uploaded_file is not None or url_input:
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    if uploaded_file is not None:
        input_path = handle_file_upload(uploaded_file, upload_dir)
    elif url_input:
        input_path = handle_url_download(url_input, upload_dir)

    output_dir = upload_dir

    if processing_option == 'Process XAPK' and input_path.endswith('.xapk'):
        st.write("Processing XAPK...")
        output_path = process_xapk(input_path)
    elif processing_option == 'Sign APK' and input_path.endswith('.apk'):
        st.write("Signing APK...")
        output_path = process_sign(input_path)
    elif processing_option == 'Debug APK' and input_path.endswith('.apk'):
        st.write("Debugging APK...")
        output_path = debug_apk(input_path, output_dir)
    elif processing_option == 'XAPK Debug' and input_path.endswith('.xapk'):
        st.write("Debugging XAPK...")
        output_path = xapk_debug(input_path, output_dir)
    else:
        st.error("The selected process is not compatible with the uploaded file type. Please ensure the file type matches your selection.")
        output_path = None

    if output_path:
        st.success("APK processed successfully!")
        st.write("Output path:")
        st.text(output_path)

        if os.path.exists(output_path):
            with open(output_path, "rb") as f:
                file_data = f.read()
                st.download_button(
                    label="Download Processed APK",
                    data=file_data,
                    file_name=os.path.basename(output_path),
                    mime="application/vnd.android.package-archive"
                )
        else:
            st.error("Processed APK file not found. Please try again.")
    else:
        st.error("Failed to process APK. Please try again.")

    cleanup_files(upload_dir)