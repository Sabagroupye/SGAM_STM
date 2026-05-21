import os
import sys
import subprocess
import time
def check_dependencies():
    print("\n" + "="*60)
    print("      SABA GROUP - SYSTEM DEPENDENCY CHECKER           ")
    print("="*60)
    py_ver = sys.version.split()[0]
    print(f" [✓] Python Environment: {py_ver}")
    # 1. Try to activate static-ffmpeg if already installed in the current environment
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
    except ImportError:
        pass

    from config import CORE_ASSETS_DIR
    ext = ".exe" if os.name == "nt" else ""
    ffmpeg_local = os.path.join(CORE_ASSETS_DIR, f"ffmpeg{ext}")
    ffmpeg_found = False
    if os.path.exists(ffmpeg_local):
        print(f" [✓] FFmpeg: Found Local Binary at {CORE_ASSETS_DIR}")
        ffmpeg_found = True
    else:
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(" [✓] FFmpeg: Found in PATH (Global / Activated)")
            ffmpeg_found = True
        except:
            print(" [!] FFmpeg: NOT FOUND in Local or PATH.")
            print(" [>] Attempting to install 'static-ffmpeg' for cross-platform support...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "static-ffmpeg"])
                import importlib
                sf = importlib.import_module("static_ffmpeg")
                sf.add_paths() 
                print(" [✓] static-ffmpeg: Installed and Activated Successfully")
                ffmpeg_found = True
            except:
                print(" [✖] static-ffmpeg: Installation Failed!")
    required_libs = {
        'mutagen': "mutagen",
        'yt_dlp': "yt-dlp",
        'psutil': "psutil",
        'PIL': "Pillow",
        'static_ffmpeg': "static-ffmpeg"
    }
    for lib_id, pip_name in required_libs.items():
        try:
            __import__(lib_id)
            print(f" [✓] Library '{pip_name}': Installed")
        except ImportError:
            print(f" [>] Library '{pip_name}': Missing. Installing now...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", pip_name])
                print(f" [✓] Library '{pip_name}': Installation Successful")
            except Exception as e:
                print(f" [✖] Library '{pip_name}': Installation Failed! ({e})")
    print("-" * 60)
    time.sleep(1)
if __name__ == "__main__":
    check_dependencies()