import subprocess
import os
import sys
from dependency_check import check_dependencies, FFMPEG, DENO

# Set your default base output folder here
DEFAULT_OUTPUT_PATH = r"C:\Video\Youtube"

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in " ._()-" else "_" for c in name)

def get_playlist_title(url):
    import yt_dlp  # imported here so the dependency check runs first
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
        sys.executable, "-m", "yt_dlp",  # same Python running this script; no PATH needed
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "--merge-output-format", "mp4",
        # Captions: prefer creator-uploaded, fall back to auto-generated.
        # --write-subs + --embed-subs together keeps the .srt file AND embeds it.
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", "en.*",
        "--convert-subs", "srt",
        "--embed-subs",
        "-o", os.path.join(output_path, "%(title).200s.%(ext)s"),
        "--progress",
        url
    ]

    result = subprocess.run(command)
    make_transcripts(output_path)
    return result.returncode == 0

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

def make_transcripts(output_path):
    """Create a .txt transcript for every .srt in the folder that doesn't have one yet."""
    for name in os.listdir(output_path):
        if name.endswith(".srt"):
            srt_path = os.path.join(output_path, name)
            if not os.path.exists(os.path.splitext(srt_path)[0] + ".txt"):
                srt_to_txt(srt_path)

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
        ok = download_with_ytdlp(url, playlist_folder)
    else:
        ok = download_with_ytdlp(url, DEFAULT_OUTPUT_PATH)

    if ok:
        print("\nAll downloads completed!")
    else:
        print("\nOne or more downloads failed - see the errors above.")

if __name__ == "__main__":
    # yt-dlp-ejs + deno are needed to solve YouTube's JavaScript challenges
    check_dependencies([("yt_dlp", "yt-dlp"), ("yt_dlp_ejs", "yt-dlp-ejs")],
                       tools=(FFMPEG, DENO))
    main()
