"""Startup check for the YouTube downloader scripts.

Makes sure the required Python packages and ffmpeg are available. Anything
missing is offered for install; declining (or a failed install) exits.
"""
import importlib.util
import os
import shutil
import subprocess
import sys

# winget puts shortcuts for installed command-line tools here. It's added to PATH
# on install, but terminals that were already open don't see that until restarted.
WINGET_LINKS = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Links")


def ask(question):
    return input(f"{question} [Y/n]: ").strip().lower() in ("", "y", "yes")


def ensure_package(module_name, pip_name=None):
    """Install a missing Python package with pip, using the Python running this script."""
    if importlib.util.find_spec(module_name):
        return
    pip_name = pip_name or module_name
    print(f"\nMissing Python package: {pip_name}")
    if not ask(f"Install {pip_name} now?"):
        sys.exit(f"Cannot continue without {pip_name}. Install it with:\n"
                 f"  \"{sys.executable}\" -m pip install {pip_name}")
    if subprocess.run([sys.executable, "-m", "pip", "install", "-U", pip_name]).returncode != 0:
        sys.exit(f"Failed to install {pip_name}.")
    importlib.invalidate_caches()


def find_tool(exe):
    """Return True if the program can be run, adding the winget folder to PATH if needed."""
    if shutil.which(exe):
        return True
    if os.path.exists(os.path.join(WINGET_LINKS, f"{exe}.exe")):
        # Installed, but this terminal predates the PATH change; fix it for this run
        os.environ["PATH"] = WINGET_LINKS + os.pathsep + os.environ["PATH"]
        return True
    return False


def ensure_tool(exe, winget_id, purpose, download_url):
    """Install a missing command-line program with winget."""
    if find_tool(exe):
        return
    print(f"\n{exe} was not found. It is needed to {purpose}.")
    if not shutil.which("winget"):
        sys.exit(f"Install {exe} from {download_url} and add it to PATH.")
    if not ask(f"Install {exe} now using winget?"):
        sys.exit(f"Cannot continue without {exe}. Install it with:\n  winget install {winget_id}")
    subprocess.run(["winget", "install", "--id", winget_id, "-e",
                    "--accept-source-agreements", "--accept-package-agreements"])
    if not find_tool(exe):
        sys.exit(f"{exe} install did not complete. Open a new terminal and run the script again.")


FFMPEG = ("ffmpeg", "Gyan.FFmpeg", "merge video/audio and handle captions",
          "https://ffmpeg.org/download.html")
DENO = ("deno", "DenoLand.Deno", "let yt-dlp get past YouTube's JavaScript checks",
        "https://deno.com")


def check_dependencies(packages, tools=(FFMPEG,)):
    """packages: list of (module_name, pip_name). tools: tuples like FFMPEG / DENO."""
    for module_name, pip_name in packages:
        ensure_package(module_name, pip_name)
    for tool in tools:
        ensure_tool(*tool)
