import yt_dlp
import os
from pathlib import Path
import sys

def get_default_path():
    # Detects if running in Termux
    if os.path.exists('/data/data/com.termux/files/home'):
        return Path('/sdcard/Download')
    # Default for Windows/Mac/Linux is the user's standard Downloads folder
    return Path.home() / "Downloads"

def run_downloader():
    default_base = get_default_path()

    print("===============================")
    print("   UNIVERSAL MEDIA DOWNLOADER  ")
    print(" (Win / Mac / Linux / Termux)  ")
    print("===============================")
    
    # [ STEP 1: CHOOSE DESTINATION ]
    print(f"\nDefault Save Folder: {default_base}")
    change_path = input("Press Enter to use default, or type a new folder path: ").strip()
    
    save_base = Path(change_path) if change_path else default_base

    # Define sub-folders
    paths = {
        'muzika': save_base / 'muzika',
        'dramas': save_base / 'dramas',
        'web': save_base / 'web'
    }

    # Create folders safely
    for p in paths.values():
        try:
            p.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"❌ Error creating folder {p}: {e}")
            return

    # [ STEP 2: CHOOSE FORMAT ]
    print("\n[ SELECT YOUR GOAL ]")
    print("1) Music (MP3) -> /muzika")
    print("2) Drama (MP4) -> /dramas")
    print("3) Web Video (MP4) -> /web")
    print("4) Playlist (MP3) -> /muzika/folder")
    print("5) Playlist (MP4) -> /dramas/folder")
    
    choice = input("\nEnter choice (1-5): ").strip()
    url = input("\nPaste your link: ").strip()

    if not url:
        print("❌ Error: No link provided!")
        return

    # Turbo settings
    ydl_opts = {
        'nocheckcertificate': True,
        'quiet': False,
        'no_warnings': True,
        'concurrent_fragment_downloads': 10,
    }

    # Logic for different choices
    if choice in ['1', '4']:
        folder = paths['muzika']
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320'}],
        })
    elif choice in ['2', '5']:
        folder = paths['dramas']
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        })
    else:
        folder = paths['web']
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        })

    # Set filename template based on single vs playlist
    if choice in ['4', '5']:
        ydl_opts['outtmpl'] = str(folder / "%(playlist_title)s" / "%(playlist_index)s - %(title)s.%(ext)s")
    else:
        ydl_opts['outtmpl'] = str(folder / "%(title)s.%(ext)s")
        ydl_opts['noplaylist'] = True

    # [ STEP 3: DOWNLOAD ]
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ SUCCESS! Files saved in: {folder}")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    run_downloader()
