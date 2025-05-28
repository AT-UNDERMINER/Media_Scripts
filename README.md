# 📚 Media Organisation

Organize and manage your digital movie library with two handy automation scripts!

This repo includes:

- **Folder & File Renamer**: Renames video files based on their parent folder name (great for Plex organization).
- **Resolution Sorter**: Sorts `.mkv` files into subfolders based on their video resolution (480p, 576p, 720p, 1080p,
  2160p).

---

## 📂 Scripts

### 1. Folder & File Renamer

**Purpose**:  
Move `.mkv` files from their individual movie folders directly into the main library folder, renaming each file to match
the folder title.

**Main Features**:

- Skips folders containing more than one `.mkv` file.
- Deletes the original folder after moving the file.
- Logs all actions (moved, deleted, skipped, errors) into `video_organizer.log`.
- Ensures Plex-friendly naming for easy metadata scraping.

**How It Works**:

```
Before: Movies/Inception (2010)/randomfile.mkv

After: Movies/Inception (2010).mkv
```

---

### 2. Resolution Sorter

**Purpose**:  
Sort `.mkv` files into subfolders based on their video resolution.

**Main Features**:

- Detects the resolution (height) of each `.mkv` file.
- Automatically moves files into one of: `480p`, `576p`, `720p`, `1080p`, `2160p`.
- Ensures clean separation of files for easier batch transcoding later.

**How It Works**:

```
Before: Movies/Inception (2010).mkv Movies/The Matrix (1999).mkv

After: Movies/1080p/Inception (2010).mkv Movies/720p/The Matrix (1999).mkv
```

---

### 3. YouTube Video Downloaders

**Purpose**:  
Download YouTube videos or playlists in full resolution (up to 1080p and higher) with audio merged and properly named
for media libraries.

**Included Scripts**:

- `youtube_downloader_pytubefix.py`
- `youtube_downloader_ytdlp.py`

---

#### 📥 `youtube_downloader_pytubefix.py`

**Main Features**:

- Uses [`pytubefix`](https://pypi.org/project/pytubefix/) to fetch and download video/audio streams.
- Downloads the **highest resolution video** and **highest bitrate audio** separately.
- Merges them using `ffmpeg` into a single `.mp4` file.
- Supports **single videos** and **playlists**.
- Automatically names files using the video title.
- If it's a playlist, it creates a folder using the playlist title to keep things organized.

**Requirements**:

- `pytubefix`
- `ffmpeg` (must be in PATH)

---

#### ⚠️ `youtube_downloader_ytdlp.py` (Advanced but Experimental)

**Main Features**:

- Uses [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — a powerful alternative for downloading from YouTube.
- Automatically selects the best video+audio formats and merges them.
- Much **faster** due to parallelized segment downloading and built-in FFmpeg support.
- Great for **large playlists or batch downloading**.

**Known Issue**:

- As of recent YouTube backend updates (May 2025), `yt-dlp` may fall back to **HLS `.ts` fragments**, causing:
    - No audio in the final file
    - Inability to **seek or fast-forward** in the video
- This is due to YouTube throttling or format blocking. It can be resolved by forcing remux with `--remux-video mp4`,
  but it is not fully reliable for all cases.

**Recommendation**:

- Use `pytubefix` for consistent results and properly merged `.mp4` files.
- Use `yt-dlp` only if you're familiar with command-line video handling or need advanced features like multi-threaded
  downloads.

## ⚙️ Requirements

- **Python 3.8+**
- **ffmpeg** installed (specifically, `ffprobe` for the Resolution Sorter script)
    - Download from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

If `ffmpeg` is not in your system PATH, you can directly edit the script to point to your `ffprobe.exe` location.

---

## 🚀 Usage

1. Clone this repository or download the scripts individually.
2. Install any necessary Python packages (no special packages required beyond standard library).
3. Edit the `source_folder` path at the top of each script to match your movie library.
4. Run the script using:

`python script_name.py`

5. Check the console output and the `video_organizer.log` file for a full action report.

---

## 🛠 Future Improvements

- Add `.mp4` and `.avi` support
- Automatic subtitle handling (burn-in or pass-through)
- Batch conversion hooks for HandBrakeCLI
- GUI version (drag & drop folders)

---

## 📄 License

This project is open source and free to use. Attribution appreciated but not required.

---

## ✨ Contributions

Feel free to open issues or PRs for improvements, bug fixes, or feature ideas!
