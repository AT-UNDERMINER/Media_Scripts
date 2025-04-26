# 📚 Media Organisation

Organize and manage your digital movie library with two handy automation scripts!

This repo includes:

- **Folder & File Renamer**: Renames video files based on their parent folder name (great for Plex organization).
- **Resolution Sorter**: Sorts `.mkv` files into subfolders based on their video resolution (480p, 576p, 720p, 1080p, 2160p).

---

## 📂 Scripts

### 1. Folder & File Renamer
**Purpose**:  
Move `.mkv` files from their individual movie folders directly into the main library folder, renaming each file to match the folder title.

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
