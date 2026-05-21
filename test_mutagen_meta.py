import os
import sys
import time
import subprocess
from config import (
    BRANDING_TEXT, COMMENT, COMPOSER, GENRE, 
    COPYRIGHT, ALBUM_ARTIST, CORE_POSTER_PATH
)
from utils import COMPANY_NAME
from internal_paths import CORE_FFMPEG

try:
    from mutagen.mp4 import MP4, MP4Cover
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, TIT2, TPE1, COMM, TCOM, TCON, TCOP, TPE2, APIC, TXXX
except ImportError:
    print("\n [!] 'mutagen' library not found. Please run 'launcher.py' first.")
    sys.exit()

def test_mutagen_mode(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    start_time = time.time()
    try:
        if ext == '.mp4':
            audio = MP4(file_path)
            audio["\xa9nam"] = BRANDING_TEXT
            audio["\xa9ART"] = COMPANY_NAME
            audio["\xa9cmt"] = COMMENT
            if os.path.exists(CORE_POSTER_PATH):
                with open(CORE_POSTER_PATH, "rb") as f:
                    audio["covr"] = [MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)]
            audio.save()
        elif ext == '.mp3':
            try: audio = ID3(file_path)
            except: audio = ID3()
            audio["TIT2"] = TIT2(encoding=3, text=BRANDING_TEXT)
            audio.save(file_path)
        return time.time() - start_time
    except Exception as e:
        return f"Error: {e}"

def test_ffmpeg_instant_mode(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    temp_out = os.path.join(os.path.dirname(file_path), f"TEMP_FFMPEG_OUT{ext}")
    start_time = time.time()
    
    cmd = [CORE_FFMPEG, "-i", file_path]
    if os.path.exists(CORE_POSTER_PATH):
        cmd.extend(["-i", CORE_POSTER_PATH, "-map", "0", "-map", "1", "-c", "copy", "-disposition:v:1", "attached_pic"])
    else:
        cmd.extend(["-map", "0", "-c", "copy"])
    
    cmd.extend([
        "-metadata", f"title={BRANDING_TEXT}",
        "-metadata", f"artist={COMPANY_NAME}",
        "-metadata", f"comment={COMMENT}",
        "-y", temp_out
    ])
    
    try:
        # Improved error reporting
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            return f"FFmpeg Error (Code {res.returncode}): {res.stderr[-200:]}"
            
        duration = time.time() - start_time
        if os.path.exists(temp_out): os.remove(temp_out)
        return duration
    except Exception as e:
        return f"System Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n [!] Usage: Drag and drop a video/audio file here.")
        input("\n Press Enter to close...")
        sys.exit()

    file_p = sys.argv[1]
    print("\n" + "="*60)
    print(f"      METADATA TEST: MUTAGEN VS FFMPEG (INSTANT)      ")
    print("="*60)
    print(f" Target: {os.path.basename(file_p)} ({os.path.getsize(file_p)/1024/1024:.2f} MB)")
    
    print("\n [1] Testing MUTAGEN (Standard Rewrite)...")
    m_res = test_mutagen_mode(file_p)
    print(f"  ➔ Mutagen Time: {m_res if isinstance(m_res, str) else f'{m_res:.4f}s'}")
    
    print("\n [2] Testing FFMPEG (Instant Copy Inject)...")
    f_res = test_ffmpeg_instant_mode(file_p)
    print(f"  ➔ FFmpeg Time: {f_res if isinstance(f_res, str) else f'{f_res:.4f}s'}")
    
    print("\n" + "-"*60)
    if not isinstance(m_res, str) and not isinstance(f_res, str):
        if f_res < m_res:
            print(f" [★] FFMPEG is {m_res/f_res:.1f}x FASTER!")
        else:
            print(f" [★] MUTAGEN is {f_res/m_res:.1f}x FASTER!")
    print("="*60)
    
    input("\n Press Enter to close...")
