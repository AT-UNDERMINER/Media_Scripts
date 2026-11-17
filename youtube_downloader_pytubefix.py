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

def srt_to_txt(srt_path):
    """Write a readable transcript next to the .srt: one '[HH:MM:SS] text' line per caption.
    Skips repeated lines, which auto-generated captions produce as they roll."""
    txt_path = os.path.splitext(srt_path)[0] + ".txt"
    with open(srt_path, encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")

    lines, last = [], None
    for block in blocks:
        parts = block.strip().splitlines()
        timing = next((i for i, p in enumerate(parts) if "-->" in p), None)
        if timing is None:
            continue
        start = parts[timing].split("-->")[0].strip().split(",")[0]  # HH:MM:SS
        for text in parts[timing + 1:]:
            text = text.strip()
            if text and text != last:
                lines.append(f"[{start}] {text}")
                last = text

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Saved transcript: {txt_path}")

def save_captions(yt, output_path, title):
    """Save English captions as .srt, preferring creator-uploaded over auto-generated.
    Returns the .srt path, or None if no English captions exist."""
    caption = yt.captions.get('en') or yt.captions.get('a.en')
    if not caption:
        # Fall back to any English variant, e.g. 'en-GB' or 'a.en-US'
        caption = next((c for c in yt.captions if c.code.removeprefix('a.').startswith('en')), None)
    if not caption:
        print("\nNo English captions available.")
        return None

    srt_file = os.path.join(output_path, f"{title}.en.srt")
    with open(srt_file, "w", encoding="utf-8") as f:
        f.write(caption.generate_srt_captions())
    print(f"\nSaved captions ({caption.code}): {srt_file}")
    srt_to_txt(srt_file)
    return srt_file

def merge_with_ffmpeg(video_path, audio_path, output_path, srt_path=None):
    print("\nMerging with FFmpeg...")
    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output if it exists
        "-i", video_path,
        "-i", audio_path,
    ]
    if srt_path:
        cmd += ["-i", srt_path]
    cmd += ["-map", "0:v", "-map", "1:a"]
    if srt_path:
        # Embed as an MP4 text track; the .srt file is kept alongside the video
        cmd += ["-map", "2:s", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng"]
    cmd += [
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

        try:
            srt_file = save_captions(yt, output_path, title)
        except Exception as e:
            print(f"\nCould not save captions, continuing without them. Error: {e}")
            srt_file = None
        merge_with_ffmpeg(video_file, audio_file, final_file, srt_file)
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
    from dependency_check import check_dependencies
    check_dependencies([("pytubefix", "pytubefix")])
    from pytubefix import YouTube, Playlist  # imported after the check so it's guaranteed present
    os.makedirs(DEFAULT_OUTPUT_PATH, exist_ok=True)
    main()
