import os
import shutil
import subprocess

# 🔧 Set your movie folder
source_folder = r"YOUR_MOVIE_FOLDER"  # <--- Change this to your movie folder path

# 📍 Direct path to ffprobe (adjust to where you installed FFmpeg)
ffprobe_path = r"C:\ffmpeg\bin\ffprobe.exe"  # <--- Change this if your path is different

# 🎯 Resolution folders to sort into
res_folders = ['480p', '576p', '720p', '1080p', '2160p']

# 📁 Create resolution folders if they don't exist
for folder in res_folders:
    os.makedirs(os.path.join(source_folder, folder), exist_ok=True)

# 🧠 Function to get video resolution using ffprobe
def get_video_resolution(filepath):
    try:
        cmd = [
            ffprobe_path, '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            filepath
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip().split('\n')
        width = int(output[0])
        height = int(output[1])
        return width, height
    except Exception as e:
        print(f"⚠️ Error reading resolution for {filepath}: {e}")
        return None, None

# 🚀 Loop through MKV files and sort by resolution
for filename in os.listdir(source_folder):
    if filename.lower().endswith('.mkv'):
        file_path = os.path.join(source_folder, filename)
        width, height = get_video_resolution(file_path)

        if height:
            if height <= 480:
                target_folder = '480p'
            elif height <= 576:
                target_folder = '576p'
            elif height <= 720:
                target_folder = '720p'
            elif height <= 1080:
                target_folder = '1080p'
            else:
                target_folder = '2160p'

            dest_path = os.path.join(source_folder, target_folder, filename)
            shutil.move(file_path, dest_path)
            print(f"✅ Moved {filename} to {target_folder}/")

print("🎉 Sorting complete.")
