import shutil

def cleanup_files(upload_dir):
    shutil.rmtree(upload_dir, ignore_errors=True)