import os
import time
from utils import print_header, clear_screen, smart_input, VIDEO_EXTS, AUDIO_EXTS, find_media, parse_dropped_paths
from video_pro import video_main_entry
from audio_pro import audio_main_entry
from fast_meta_pro import quick_sweep
from renamer_pro import smart_renamer_ui
def reception_menu(raw_paths, v_files, a_files):
    from utils import find_media, parse_dropped_paths
    valid_items = list(raw_paths)
    while True:
        media = find_media(valid_items)
        v_list = [f for f in media if f.lower().endswith(VIDEO_EXTS)]
        a_list = [f for f in media if f.lower().endswith(AUDIO_EXTS)]
        common_parent = os.getcwd()
        if valid_items:
            try:
                paths_to_check = [p for p in valid_items if os.path.exists(p)]
                common_parent = os.path.dirname(paths_to_check[0]) if len(paths_to_check) == 1 else os.path.commonpath(paths_to_check)
            except: pass
        print_header("RECEPTION HUB", f"{len(valid_items)} ITEMS IN RECORD")
        print(f" [🔍] Current Content Statistics:")
        print(f"  • Video Files: {len(v_list)}")
        print(f"  • Audio Files: {len(a_list)}")
        print(f"  • Total Items: {len(valid_items)} (Files/Folders)")
        print("-" * 70)
        print("\n SELECT OPERATION:")
        options = []
        if v_list: options.append(("VIDEO PRODUCTION (Branding, Censor, Quality)", "VIDEO"))
        if a_list: options.append(("AUDIO PRODUCTION (Mixing, Quality, Tags)", "AUDIO"))
        options.append(("SMART RENAMER    (Clean/Replace Filenames)", "RENAMER"))
        options.append(("METADATA SWEEP   (Instant Metadata Update)", "METADATA"))
        for i, (label, _) in enumerate(options, 1):
            print(f"  {i} ➔ {label}")
        print("  B ➔ [BACK TO MAIN HUB]")
        print("-" * 70)
        print(" [💡] Tip: You can DRAG & DROP more files/folders here to ADD them!")
        choice = smart_input("\n ► Selection or Drop More: ")
        if not choice: continue
        if choice == '__BACK__' or choice.upper() == 'B': break
        if (":" in choice or "\\" in choice or "/" in choice) and len(choice) > 5:
            new_raw = parse_dropped_paths(choice)
            if new_raw:
                ans = smart_input(f" \n [?] {len(valid_items)} items exist. Clear previous? (Y/N) [N]: ").upper() or 'N'
                if ans == '__BACK__': continue
                if ans == 'Y': valid_items = new_raw
                else: valid_items.extend(new_raw)
            continue
        try:
            idx = int(choice) - 1
            if idx < 0: continue
            label, action = options[idx]
        except: continue
        if action == "RENAMER":
            smart_renamer_ui(valid_items)
        elif action == "METADATA":
            quick_sweep(media, common_parent)
        elif action == "VIDEO":
            video_main_entry(v_list, common_parent, is_folder_mode=any(os.path.isdir(p) for p in valid_items))
        elif action == "AUDIO":
            audio_main_entry(a_list, common_parent, is_folder_mode=any(os.path.isdir(p) for p in valid_items))
        print("\n [✓] Task completed. Returning to reception hub..."); time.sleep(1.5)