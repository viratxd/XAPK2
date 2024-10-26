import subprocess
import streamlit as st
import os  
def debug_apk(input_path, output_dir): 
    command = f"apk-mitm {input_path} -o {output_dir}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        output_file_name = result.stdout.split("Patched file: ")[-1].strip()
        output_path = os.path.join(output_dir, output_file_name)
        return output_path
    else:
        st.error(f"Error debugging APK: {result.stderr}")
        return None