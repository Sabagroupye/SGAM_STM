import os
import sys
import time
from utils import find_media, clear_screen, smart_input, VIDEO_EXTS, AUDIO_EXTS
from video_pro import video_main_entry
from audio_pro import audio_main_entry
from fast_meta_pro import quick_sweep
from renamer_pro import smart_renamer_ui
def folder_reception_entry(raw_paths):
    valid_paths = [os.path.abspath(p) for p in raw_paths if os.path.isdir(p)]
    if not valid_paths:
        print("\n [!] No valid folders detected. Returning..."); time.sleep(2); return
    common_parent = os.path.dirname(valid_paths[0]) if len(valid_paths) == 1 else os.path.commonpath(valid_paths)
    def handle_subfolder_cleaning(paths):
        has_sub = False
        for p in paths:
            for _, dirs, _ in os.walk(p):
                if dirs: has_sub = True; break
            if has_sub: break
        if has_sub:
            ans = smart_input("\n ► Clean subfolders? (Y/N) [N]: ").upper() or 'N'
            if ans == '__BACK__': return
            if ans == 'Y':
                print(" [⏳] Cleaning subfolder names...")
                from utils import sanitize_name
                for p in paths:
                    for root, dirs, _ in os.walk(p, topdown=False):
                        for d in dirs:
                            old_d_path = os.path.join(root, d)
                            new_d_name = sanitize_name(d)
                            if d != new_d_name:
                                new_d_path = os.path.join(root, new_d_name)
                                try:
                                    if not os.path.exists(new_d_path): os.rename(old_d_path, new_d_path)
                                except: pass
    while True:
        clear_screen()
        media = find_media(valid_paths)
        v_files = [f for f in media if f.lower().endswith(VIDEO_EXTS)]
        a_files = [f for f in media if f.lower().endswith(AUDIO_EXTS)]
        from utils import print_header
        print_header("FOLDER HUB", f"{len(valid_paths)} FOLDERS READY")
        print(f" [📂] Folders  : {len(valid_paths)}")
        print(f" [🔍] Found    : {len(v_files)} Videos | {len(a_files)} Audios")
        print("-" * 70)
        print("\n SELECT OPERATION:")
        menu_options = []
        if v_files: menu_options.append(("VIDEO PRODUCTION (Logo, Layers, Quality)", "VIDEO"))
        if a_files: menu_options.append(("AUDIO PRODUCTION (Mixing, Quality, Tags)", "AUDIO"))
        menu_options.append(("SMART RENAMER    (Clean/Replace Names)", "RENAMER"))
        menu_options.append(("METADATA SWEEP   (Instant In-Place Tags)", "METADATA"))
        for i, (label, _) in enumerate(menu_options, 1):
            print(f"  {i} ➔ {label}")
        print("  B ➔ [BACK TO HUB]")
        print("-" * 70)
        print(" [💡] Tip: You can DRAG & DROP more folders here to add them!")
        choice = smart_input("\n ► Selection or Drop Folders: ")
        if not choice: continue
        if (":" in choice or "\\" in choice or "/" in choice) and len(choice) > 5:
            from utils import parse_dropped_paths
            new_raw = parse_dropped_paths(choice)
            new_v_paths = [os.path.abspath(p) for p in new_raw if os.path.isdir(p)]
            if new_v_paths:
                print("\n" + "!"*45)
                ans = smart_input(f" [?] {len(valid_paths)} folders exist. Clear? (Y/N) [Y]: ").upper() or 'Y'
                if ans == '__BACK__': continue
                if ans == 'Y':
                    valid_paths = new_v_paths
                    common_parent = os.path.dirname(valid_paths[0]) if len(valid_paths) == 1 else os.path.commonpath(valid_paths)
                else:
                    valid_paths.extend(new_v_paths)
                    try: common_parent = os.path.commonpath(valid_paths)
                    except: pass
            continue
        if choice == '__BACK__' or choice.upper() == 'B': break
        try:
            idx = int(choice) - 1
            label, action = menu_options[idx]
        except: continue
        handle_subfolder_cleaning(valid_paths)
        if action == "RENAMER":
            smart_renamer_ui(valid_paths)
        elif action == "METADATA":
            quick_sweep(media, common_parent)
        elif action == "VIDEO":
            video_main_entry(v_files, common_parent, is_folder_mode=True)
        elif action == "AUDIO":
            audio_main_entry(a_files, common_parent, is_folder_mode=True)
        print("\n [✓] Task completed. Returning to folder menu..."); time.sleep(1)
if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit()
    folder_reception_entry(sys.argv[1:])