import gradio as gr
import os
from utils.apk_debug import debug_apk
from utils.apk_process import process_xapk, process_sign, xapk_debug
from utils.file_handling import handle_file_upload, handle_url_download
from utils.cleanup import cleanup_files  # You can call this later if needed

def process_apk(uploaded_file, url_input, processing_option):
    # Check if either file or URL is provided
    if uploaded_file is None and (url_input is None or url_input.strip() == ""):
        return "No file or URL provided.", None

    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Use the uploaded file if available, otherwise use the URL input.
    if uploaded_file is not None:
        # In Gradio, uploaded_file is a dictionary-like object with a 'name' key and binary data.
        input_path = handle_file_upload(uploaded_file, upload_dir)
    else:
        input_path = handle_url_download(url_input, upload_dir)

    output_dir = upload_dir
    output_path = None

    # Choose the processing function based on the selected option and file type.
    if processing_option == 'Process XAPK' and input_path.endswith('.xapk'):
        print("Processing XAPK...")
        output_path = process_xapk(input_path)
    elif processing_option == 'Sign APK' and input_path.endswith('.apk'):
        print("Signing APK...")
        output_path = process_sign(input_path)
    elif processing_option == 'Debug APK' and input_path.endswith('.apk'):
        print("Debugging APK...")
        output_path = debug_apk(input_path, output_dir)
    elif processing_option == 'XAPK Debug' and input_path.endswith('.xapk'):
        print("Debugging XAPK...")
        output_path = xapk_debug(input_path, output_dir)
    else:
        return ("The selected process is not compatible with the uploaded file type. "
                "Please ensure the file type matches your selection."), None

    # Check if the output file exists and return it for download.
    if output_path and os.path.exists(output_path):
        message = f"APK processed successfully! Output path: {output_path}"
        # Optionally, if you want to clean up after download, you can do it here or in a separate process.
        # cleanup_files(upload_dir)
        return message, output_path
    else:
        return "Failed to process APK. Please try again.", None

# Build the Gradio interface using Blocks for a modern layout.
with gr.Blocks() as demo:
    gr.Markdown("# ANDROID APP DEBUGGING")
    
    with gr.Row():
        uploaded_file = gr.File(label="Upload APK file", file_types=["apk", "xapk", "apks"])
        url_input = gr.Textbox(label="Or enter APK URL")
    
    processing_option = gr.Radio(
        choices=['Process XAPK', 'Sign APK', 'Debug APK', 'XAPK Debug'],
        label="Choose the processing type:"
    )
    
    process_button = gr.Button("Process APK")
    status_output = gr.Textbox(label="Status")
    file_output = gr.File(label="Download Processed APK")
    
    process_button.click(
        fn=process_apk,
        inputs=[uploaded_file, url_input, processing_option],
        outputs=[status_output, file_output]
    )

if __name__ == "__main__":
    # Use the PORT environment variable if available; otherwise default to 7860.
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
