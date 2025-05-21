import subprocess
import os
import sys
import yt_dlp  # used to fetch metadata (not for downloading)

# Set your default base output folder here
DEFAULT_OUTPUT_PATH = r"C:\Video\Youtube"

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in " ._()-" else "_" for c in name)

def get_playlist_title(url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return sanitize_filename(info.get('title', 'playlist'))
    except Exception as e:
        print(f"Could not fetch playlist title: {e}")
        return "playlist"

def download_with_ytdlp(url, output_path):
    os.makedirs(output_path, exist_ok=True)
    print(f"\nDownloading from: {url}")
    print(f"Saving to: {output_path}\n")

    command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "--merge-output-format", "mp4",
        "-o", os.path.join(output_path, "%(title).200s.%(ext)s"),
        "--progress",
        url
    ]

    process = subprocess.Popen(command)
    process.communicate()

def is_playlist(url):
    return 'playlist?' in url.lower() or 'list=' in url.lower()

def main():
    url = input("Enter YouTube video or playlist URL: ").strip()
    if not url:
        print("No URL provided.")
        return

    if is_playlist(url):
        playlist_title = get_playlist_title(url)
        playlist_folder = os.path.join(DEFAULT_OUTPUT_PATH, playlist_title)
        download_with_ytdlp(url, playlist_folder)
    else:
        download_with_ytdlp(url, DEFAULT_OUTPUT_PATH)

    print("\nAll downloads completed!")

if __name__ == "__main__":
    main()
