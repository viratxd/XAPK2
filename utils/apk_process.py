import os
import subprocess
import shutil
import zipfile
import streamlit as st
from utils.apk_debug import debug_apk

def process_xapk(xapk_path):
    try:
        folder = os.path.dirname(xapk_path)
        name_without_ext = os.path.splitext(os.path.basename(xapk_path))[0]
        zip_path = os.path.join(folder, f"{name_without_ext}.zip")
        extract_dir = os.path.join(folder, name_without_ext)
        
        shutil.move(xapk_path, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        os.remove(zip_path)
        
        command = f'java -jar APKEditor.jar m -i "{extract_dir}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            merged_apk_path = os.path.join(folder, f"{name_without_ext}_merged.apk")
            st.write(f"Merged APK created at: {merged_apk_path}")
            signed_apk_path = process_sign(merged_apk_path)
            return signed_apk_path
        else:
            st.error(f"Error merging APK: {result.stderr}")
            return None
            
    except Exception as e:
        st.error(f"Error processing XAPK: {str(e)}")
        shutil.rmtree(extract_dir, ignore_errors=True)
        return None

def process_sign(apk_path):
    folder = os.path.dirname(apk_path)
    command = f"java -jar uber-apk-signer.jar --apks {apk_path}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        signed_apk_path = apk_path.replace('.apk', '-aligned-debugSigned.apk')
        if os.path.exists(signed_apk_path):
            st.write("APK signing successful!")
            return signed_apk_path
        else:
            st.error("APK signing completed, but the signed file could not be found.")
            return None
    else:
        st.error(f"Error signing APK: {result.stderr}")
        return None

def xapk_debug(xapk_path, output_dir):
    # Process the XAPK file first
    signed_apk_path = process_xapk(xapk_path)
    
    if signed_apk_path:
        # Use the signed APK as input for debugging
        debug_path = debug_apk(signed_apk_path, output_dir)
        return debug_path
    else:
        st.error("Failed to process XAPK for debugging.")
        return None