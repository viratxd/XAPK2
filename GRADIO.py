import gradio as gr
import os
from utils.apk_debug import debug_apk
from utils.apk_process import process_xapk, process_sign, xapk_debug
from utils.file_handling import handle_file_upload
from utils.cleanup import cleanup_files

def process_apk(uploaded_file, processing_option):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Require an uploaded file
    if uploaded_file is None:
        return "No file provided.", None

    # Handle the uploaded file
    input_path = handle_file_upload(uploaded_file, upload_dir)
    output_dir = upload_dir
    output_path = None

    # Process based on option and file type
    try:
        if processing_option == 'Process XAPK' and input_path.lower().endswith('.xapk'):
            output_path = process_xapk(input_path)
        elif processing_option == 'Sign APK' and input_path.lower().endswith('.apk'):
            output_path = process_sign(input_path)
        elif processing_option == 'Debug APK' and input_path.lower().endswith('.apk'):
            output_path = debug_apk(input_path, output_dir)
        elif processing_option == 'XAPK Debug' and input_path.lower().endswith('.xapk'):
            output_path = xapk_debug(input_path, output_dir)
        else:
            return ("The selected process is not compatible with the uploaded file type. "
                    "Please ensure the file type matches your selection."), None

        if output_path and os.path.exists(output_path):
            return f"APK processed successfully! Output: {output_path}", output_path
        return "Failed to process APK. No output generated.", None
    except Exception as e:
        return f"Error during processing: {str(e)}", None

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# ANDROID APP DEBUGGING\nSupported file types: .apk, .xapk, .apks")
    
    uploaded_file = gr.File(label="Upload APK file", file_types=["apk", "xapk", "apks"])
    
    processing_option = gr.Radio(
        choices=['Process XAPK', 'Sign APK', 'Debug APK', 'XAPK Debug'],
        label="Choose the processing type:"
    )
    
    process_button = gr.Button("Process APK")
    status_output = gr.Textbox(label="Status")
    file_output = gr.File(label="Download Processed APK")
    
    process_button.click(
        fn=process_apk,
        inputs=[uploaded_file, processing_option],
        outputs=[status_output, file_output]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
