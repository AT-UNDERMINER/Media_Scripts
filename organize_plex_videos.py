import os
import shutil
from datetime import datetime
import stat

# Your main movie folder
main_dir = r"MOVIE_FOLDER_PATH"  # Replace with your actual path
log_file_path = os.path.join(os.path.dirname(__file__), "video_organizer.log")

# Video file types to allow
video_extensions = ('.mkv', '.mp4')

# Log function with timestamps
def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}\n"
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(entry)
    print(entry.strip())

# Handle read-only file deletion
def handle_remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# Main processing loop
for folder_name in os.listdir(main_dir):
    folder_path = os.path.join(main_dir, folder_name)

    if os.path.isdir(folder_path):
        all_files = os.listdir(folder_path)
        video_files = [f for f in all_files if f.lower().endswith(video_extensions)]

        # Process only if exactly one video file and nothing else
        if len(all_files) == 1 and len(video_files) == 1:
            video_file = video_files[0]
            old_file_path = os.path.join(folder_path, video_file)
            file_ext = os.path.splitext(video_file)[1]
            new_file_name = f"{folder_name}{file_ext}"
            new_file_path = os.path.join(main_dir, new_file_name)

            try:
                shutil.move(old_file_path, new_file_path)
                log(f"[MOVED] '{video_file}' -> '{new_file_name}'")

                shutil.rmtree(folder_path, onerror=handle_remove_readonly)
                log(f"[DELETED] Folder '{folder_name}' removed")
            except Exception as e:
                log(f"[ERROR] Failed to process folder '{folder_name}': {e}")
        else:
            log(f"[SKIPPED] Folder '{folder_name}' has unexpected files: {all_files}")
