import streamlit as st
import os
import subprocess
import shutil

# Function to process APK file
def process_apk(input_path, output_dir):
    # Run apk-mitm command
    command = f"apk-mitm {input_path} -o {output_dir}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result

# Streamlit app interface
st.title("APK File Processor")

# File upload
uploaded_file = st.file_uploader("Upload APK file", type="apk")
if uploaded_file is not None:
    # Create directories if they don't exist
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Save uploaded file
    input_path = os.path.join(upload_dir, uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
    
    # Define output directory for the patched APK
    output_dir = upload_dir

    # Process APK
    st.write("Processing APK...")
    result = process_apk(input_path, output_dir)
    
    if result.returncode == 0:
        st.success("APK processed successfully!")
        st.write("Processing result:")
        st.text(result.stdout)
        
        # Extract the patched APK file name from the stdout
        output_file_name = result.stdout.split("Patched file: ")[-1].strip()
        output_path = os.path.join(output_dir, output_file_name)
        
        # Check if the processed APK file exists
        if os.path.exists(output_path):
            st.write(f"Processed APK file found at: {output_path}")
            
            # Provide download link for the patched APK file
            with open(output_path, "rb") as f:
                file_data = f.read()
                if file_data:
                    st.write("File data read successfully.")
                    st.download_button(
                        label="Download Patched APK",
                        data=file_data,
                        file_name=os.path.basename(output_path),
                        mime="application/vnd.android.package-archive"
                    )
                else:
                    st.error("Failed to read file data.")
        else:
            st.error("Processed APK file not found. Please try again.")
    else:
        st.error(f"Error processing APK: {result.stderr}")
    
    # Clean up the uploaded and processed files
    def cleanup_files(input_path, output_path):
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

    cleanup_files(input_path, output_path)