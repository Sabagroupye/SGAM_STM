import os
import sys
import time
import traceback
from utils import clear_screen, smart_input
def main_dispatcher():
    try:
        from dependency_manager import check_dependencies
        check_dependencies()
        from utils import apply_cpu_priority
        apply_cpu_priority()
    except: pass
    print("\n [⏳] SGAM System Booting Up...")
    try:
        from internal_paths import CORE_ASSETS_DIR
        from settings_ui import system_settings_ui
        from utils import parse_dropped_paths, find_media, VIDEO_EXTS, AUDIO_EXTS
        if not os.path.exists(CORE_ASSETS_DIR):
            try: os.makedirs(CORE_ASSETS_DIR)
            except: pass
    except Exception as e:
        print(f"\n [!] BOOT ERROR (Import Phase): {e}")
        traceback.print_exc()
        input("\n Press Enter to exit...")
        return
    raw_paths = []
    if len(sys.argv) > 1:
        raw_paths = parse_dropped_paths(" ".join(sys.argv[1:]))
    while True:
        try:
            if not raw_paths:
                clear_screen()
                print("="*75)
                print("   ███████╗ ██████╗  █████╗ ███╗   ███╗    ███████╗████████╗███╗   ███╗")
                print("   ██╔════╝██╔════╝ ██╔══██╗████╗ ████║    ██╔════╝╚══██╔══╝████╗ ████║")
                print("   ███████╗██║  ███╗███████║██╔████╔██║    ███████╗   ██║   ██╔████╔██║")
                print("   ╚════██║██║   ██║██╔══██║██║╚██╔╝██║    ╚════██║   ██║   ██║╚██╔╝██║")
                print("   ███████║╚██████╔╝██║  ██║██║ ╚═╝ ██║    ███████║   ██║   ██║ ╚═╝ ██║")
                print("   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝   ╚═╝   ╚═╝     ╚═╝")
                print("="*75)
                print("  SGAM STMEDIA | v1.26.05 | @SABAGROUPYE | +967 770574579 | Edition 1 2026.05 ")
                print("="*75)
                print("\n [READY] Please drag and drop Folders or Multiple Media files here.")
                print("-" * 70)
                print(" [V] » VIDEO HUB  (Branding, Censor, Quality)")
                print(" [A] » AUDIO HUB  (Mixing, Tags, Clips)")
                print(" [S] » CARD HUB   (Manage Presets/Cards)")
                print(" [Y] » YOUTUBE    (Pro Downloader)")
                print(" [C] » CONFIG     (Global System Settings)")
                print(" [Q] » Exit")
                p_in = smart_input("\n ► Drop Paths or Action: ")
                if not p_in: continue
                if p_in.upper() == 'Q': break
                if p_in.upper() == 'S':
                    from video_card_pro import manage_video_cards
                    from audio_card_pro import manage_audio_cards
                    from utils import print_header
                    while True:
                        clear_screen()
                        print_header("CARD MANAGER", "SELECT HUB TYPE")
                        print(" 1] VIDEO Cards | 2] AUDIO Cards | 3] CONFIG | B] Back")
                        c_ans = smart_input("\n ► Selection: ").upper()
                        if c_ans == '__BACK__' or c_ans == 'B': break
                        if c_ans == '1': manage_video_cards()
                        elif c_ans == '2': manage_audio_cards()
                        elif c_ans == '3': system_settings_ui()
                    continue
                if p_in.upper() == 'V':
                    clear_screen()
                    from video_pro import video_main_entry
                    video_main_entry([], os.getcwd()); continue
                if p_in.upper() == 'A':
                    clear_screen()
                    from audio_pro import audio_main_entry
                    audio_main_entry([], os.getcwd()); continue
                if p_in.upper() == 'Y':
                    clear_screen()
                    from youtube_downloader import download_youtube_video
                    download_youtube_video(); continue
                if p_in.upper() == 'C':
                    clear_screen()
                    system_settings_ui(); continue
                raw_paths = parse_dropped_paths(p_in)
            if not raw_paths: continue
            if raw_paths:
                from utils import find_media, VIDEO_EXTS, AUDIO_EXTS
                media = find_media(raw_paths)
                v_files = [f for f in media if f.lower().endswith(VIDEO_EXTS)]
                a_files = [f for f in media if f.lower().endswith(AUDIO_EXTS)]
                if len(raw_paths) > 1 or any(os.path.isdir(p) for p in raw_paths):
                    from reception_hub import reception_menu
                    reception_menu(raw_paths, v_files, a_files)
                    raw_paths = []; continue
                if v_files:
                    from video_pro import video_main_entry
                    video_main_entry(v_files, os.getcwd())
                    raw_paths = []; continue
                if a_files:
                    from audio_pro import audio_main_entry
                    audio_main_entry(a_files, os.getcwd())
                    raw_paths = []; continue
                if raw_paths:
                    from renamer_pro import smart_renamer_ui
                    smart_renamer_ui(raw_paths)
                    raw_paths = []; continue
            raw_paths = []
            sys.argv = [sys.argv[0]]
        except KeyboardInterrupt:
            raw_paths = []
            continue
        except Exception as e:
            print(f"\n [!] HUB ERROR: {e}")
            traceback.print_exc()
            smart_input("\n [ENTER] Continue...")
            raw_paths = []
if __name__ == "__main__":
    try:
        main_dispatcher()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as fatal:
        print("\n [!!!] FATAL ERROR [!!!]")
        traceback.print_exc()
        smart_input("\n Press Enter to exit...")