from pytubefix import YouTube, Playlist
import os
import sys
import subprocess

DEFAULT_OUTPUT_PATH = r"C:\Video\Youtube"

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = int((bytes_downloaded / total_size) * 100)
    sys.stdout.write(f"\rDownloading: {progress}%")
    sys.stdout.flush()

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in " ._()-" else "_" for c in name)

def merge_with_ffmpeg(video_path, audio_path, output_path):
    print("\nMerging with FFmpeg...")
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output if it exists
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(video_path)
    os.remove(audio_path)
    print(f"Merged to: {output_path}")

def download_video(video_url, output_path=DEFAULT_OUTPUT_PATH):
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        title = sanitize_filename(yt.title)
        print(f"\nStarting download: {title}")

        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

        video_file = os.path.join(output_path, f"{title}_video.mp4")
        audio_file = os.path.join(output_path, f"{title}_audio.mp4")
        final_file = os.path.join(output_path, f"{title}.mp4")

        video_stream.download(output_path=output_path, filename=os.path.basename(video_file))
        audio_stream.download(output_path=output_path, filename=os.path.basename(audio_file))

        merge_with_ffmpeg(video_file, audio_file, final_file)
        print(f"Finished: {title}\n")

    except Exception as e:
        print(f"\nFailed to download {video_url}. Error: {e}\n")

def is_playlist(url):
    return 'playlist' in url.lower()

def main():
    url = input("Enter YouTube video or playlist URL: ").strip()

    if is_playlist(url):
        playlist = Playlist(url)
        print(f"\nFound playlist: {playlist.title}")
        print(f"Total videos: {len(playlist.video_urls)}\n")
        for video_url in playlist.video_urls:
            download_video(video_url)
    else:
        download_video(url)

    print("All downloads completed!")

if __name__ == "__main__":
    os.makedirs(DEFAULT_OUTPUT_PATH, exist_ok=True)
    main()
