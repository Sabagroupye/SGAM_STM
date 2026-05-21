import os
import sys
import traceback
import time
import random
try:
    import msvcrt
except ImportError:
    msvcrt = None
from utils import (find_media, get_output_path, run_ffmpeg, get_video_info, 
                   prepare_file_for_processing, timestamp_to_seconds, get_smart_filename, 
                   log_event, parse_dropped_paths, extract_segments_as_clips, 
                   get_binary_path, ensure_unique_path, clear_screen, print_header, 
                   smart_input, VIDEO_EXTS, AUDIO_EXTS)
from audio_logic import assemble_audio_command
from metadata import apply_instant_metadata
from config import *
import config
from internal_paths import *
from settings_manager import load_all_settings
def audio_reception_menu(file_count):
    print_header("AUDIO HUB", f"{file_count} FILES READY")
    print(" 1) 🚀 FULL PRODUCTION  (Quality + Signature Mixing + Tags)")
    print(" 2) 🔄 CONVERT/TRANSCODE (Change Format / Quality)")
    print(" 3) ✂️  SMART CLIP       (Partial Extraction / Trimming)")
    print(" 4) 🏷️  METADATA ONLY    (Instant Tagging - No Re-encode)")
    print("-" * 70)
    print(" [B] 🔙 BACK TO HUB")
    print("-" * 70)
    ans = smart_input(" ➤ Select Operation [1-4]: ").upper()
    return 'B' if ans == '__BACK__' else ans
def run_audio_batch(files, root, mode, force_local=False, is_folder_mode=False):
    from utils import launch_cpu_monitor
    launch_cpu_monitor()
    op_names = {
        '1': "FULL PRODUCTION", '2': "CONVERT/TRANSCODE", 
        '3': "SMART CLIP", '4': "METADATA ONLY"
    }
    current_op = op_names.get(mode, "AUDIO PRODUCTION")
    if mode == '4':
        print_header(current_op)
        ans = smart_input("\n ► Clean names? (Y/N) [Y]: ").upper() or 'Y'
        if ans == '__BACK__': return
        do_clean = (ans == 'Y')
        print(f"\n [🏷️] Processing {len(files)} files...")
        success, failed = 0, 0
        t_start = time.time()
        for i, f in enumerate(files, 1):
            try:
                sanitized = prepare_file_for_processing(f, is_metadata_only=True, do_clean=do_clean)
                if apply_instant_metadata(sanitized, config.CORE_POSTER_PATH):
                    success += 1
                else: failed += 1
                print(f" [{i}/{len(files)}] Done: {os.path.basename(sanitized)}".ljust(100), end="\r")
            except: failed += 1
        t_total = time.time() - t_start
        if config.FINISH_SOUND_ALERT:
            try:
                import winsound
                winsound.Beep(1000, 600)
            except: pass
        print("\n" + "="*50)
        print("          METADATA SWEEP REPORT           ")
        print("="*50)
        print(f"  [+] Success     : {success}")
        print(f"  [-] Failed      : {failed}")
        print(f"  [@] Time Taken  : {int(t_total)}s")
        print("="*50)
        smart_input("\n ► Press Enter to return...")
        return
    print_header(current_op)
    presets = load_all_settings()
    audio_cards = {k: v for k, v in presets.items() if v.get('card_type') == "Audio Card"}
    s = {}
    if mode == '2':
        print("\n [🔄] CONVERT STRATEGY:")
        print("  1 ➔ Convert Format (Same Original Quality)")
        print("  2 ➔ Change Quality (Using Audio Cards)")
        print("  B ➔ [BACK]")
        c_mode = smart_input("\n ► Selection [1]: ").upper() or "1"
        if c_mode == 'B' or c_mode == '__BACK__': return
        if c_mode == '1':
            s = {'card_name': 'Original-Quality', 'bitrate': 'Auto'}
        else:
            if not audio_cards:
                print("\n [!] No Audio Cards found. Please create one."); time.sleep(1); return
            print(f"\n [■] Select Audio Card (or B to go back):")
            names = list(audio_cards.keys())
            for i, n in enumerate(names, 1): print(f"  {i} ➔ {n}")
            idx = smart_input("\n ► Selection: ").upper()
            if idx == 'B' or idx == '__BACK__': return
            try: s = audio_cards[names[int(idx)-1]]
            except: print("\n [!] Invalid selection."); time.sleep(0.5); return
    else:
        if not audio_cards:
            print("\n [!] No Audio Cards found. Please create one."); time.sleep(1); return
        print(f"\n [■] Select Audio Card (or B to go back):")
        names = list(audio_cards.keys())
        for i, n in enumerate(names, 1): print(f"  {i} ➔ {n}")
        idx = smart_input("\n ► Selection: ").upper()
        if idx == 'B' or idx == '__BACK__': return
        try: s = audio_cards[names[int(idx)-1]]
        except: print("\n [!] Invalid selection."); time.sleep(0.5); return
    print_header(current_op, "SAVE STRATEGY")
    save_choice = "1"
    config_out_path = os.path.join(config.GLOBAL_CLIPS_OUTPUT_PATH, "Audio_Clips") if mode == '3' and config.GLOBAL_CLIPS_OUTPUT_PATH else config.AUDIO_OUTPUT_PATH
    if not force_local:
        print("\n [!] Save Strategy:")
        print("  1 ➔ In New Folder (SGAM_STMEDIA_Output)")
        print("  2 ➔ Save in Same Folder (Local Mode)")
        if config_out_path:
            print(f"  3 ➔ Default Folder (Config): {os.path.basename(config_out_path)}")
        print("  B ➔ [BACK]")
        valid_choices = ['1', '2', 'B']
        if config_out_path: valid_choices.append('3')
        save_choice = smart_input(f"\n ► Your Choice [1] {'[3]' if config_out_path else ''} [B: Back]: ").upper() or "1"
        if save_choice == 'B' or save_choice == '__BACK__': return
        if save_choice not in valid_choices: save_choice = "1"
    else:
        save_choice = "2"
    local_save_mode = (save_choice == '2')
    global_config_mode = (save_choice == '3')
    do_full_mirror = False
    do_clean_assets = False
    if not local_save_mode and is_folder_mode and root and os.path.isdir(root):
        has_sub = False
        for _, dirs, f_in in os.walk(root):
            if "SGAM_STMEDIA_Output" in _: continue
            if dirs or len(f_in) > len(files):
                has_sub = True; break
        if has_sub:
            print("\n" + "-"*45)
            print(" [?] FULL MIRROR OPTION:")
            print("  The source folder has subfolders or extra files (images, etc.).")
            print("  Do you want to create an identical copy of the full structure")
            print("  in the output folder, including non-media files? (Y/N)")
            m_ans = smart_input("\n ► Create Full Mirror? [N]: ").upper() or "N"
            if m_ans == '__BACK__': return
            if m_ans == 'Y':
                do_full_mirror = True
                print(" [⏳] Preparing Full Mirror Structure...")
                ans = smart_input("\n ► Clean mirrored assets? (Y/N) [N]: ").upper() or 'N'
                if ans == '__BACK__': return
                do_clean_assets = (ans == 'Y')
                out_root_target = os.path.join(config_out_path if global_config_mode else root, "SGAM_STMEDIA_Output")
                from utils import clone_structure
                clone_structure(root, out_root_target, do_clean=do_clean_assets)
    custom_folder = ""
    if mode == '3' and not global_config_mode:
        custom_folder = smart_input(f" ► Enter Clip Folder Name [{config.DEFAULT_CLIPS_DIR_NAME}]: ")
        if custom_folder == '__BACK__': return
        if not custom_folder: custom_folder = config.DEFAULT_CLIPS_DIR_NAME
    trim_data = None
    if mode == '3':
        print("\n [✂] CLIP MODE:")
        print(f"  1 ➔ Range  (Start/End Times)")
        print(f"  2 ➔ Random (Fixed {config.DEFAULT_CLIP_DURATION}s segment)")
        print("  B ➔ [BACK]")
        cm = smart_input(f"\n ► Mode [1]: ").upper() or "1"
        if cm == 'B' or cm == '__BACK__': return
        if cm == '1':
            print("\n [ TIMING FORMATS ]")
            print("  • 30-60         (From 30s to 60s)")
            print("  • 01:00-01:30   (From 1m to 1m 30s)")
            print("  • 10            (10s from start)")
            t_in = smart_input("\n ► Enter Timing [B: Back]: ").upper()
            if t_in == 'B' or t_in == '__BACK__': return
            if t_in:
                try: 
                    b = t_in.split('-')
                    trim_data = {'mode': 'Range', 'start': b[0], 'end': b[1] if len(b)>1 else 0}
                except: pass
            else:
                trim_data = {'mode': 'Range', 'start': config.DEFAULT_CLIP_DURATION, 'end': 0}
        else:
            trim_data = {'mode': 'Random', 'duration': config.DEFAULT_CLIP_DURATION}

    success, skipped = 0, 0
    t_start = time.time()
    skipped_list = []
    log_file_name = "sg_processed.txt"
    target_quality_tag = s.get('bitrate', config.AUDIO_QUALITY)
    apply_sig_choice = config.AUDIO_SIGNATURE_AUTO
    print("\n [🎵] AUDIO SIGNATURE (REMIX):")
    print(f"  Current Config: {'ENABLED' if apply_sig_choice == 'Yes' else 'DISABLED'}")
    ans = smart_input(" ► Apply Signature? [Y/N/Enter]: ").upper()
    if ans == '__BACK__': return
    if ans == 'Y': apply_sig_choice = 'Yes'
    elif ans == 'N': apply_sig_choice = 'No'
    is_sig_active = (apply_sig_choice == 'Yes')
    for i, f in enumerate(files, 1):
        if msvcrt and msvcrt.kbhit():
            if msvcrt.getch().upper() == b'B':
                print("\n [!] Batch cancelled by user.")
                break
        fname = os.path.basename(f)
        final_out = ""
        try:
            current_op_tag = ""
            is_meta_mode = (mode == '4')
            sanitized_f = prepare_file_for_processing(f, is_metadata_only=is_meta_mode, op_tag=current_op_tag)
            v_dir = os.path.dirname(sanitized_f)
            v_name = os.path.basename(sanitized_f)
            fname = v_name
            processed_log_path = os.path.join(v_dir, log_file_name)
            raw_br = s.get('bitrate', config.AUDIO_QUALITY)
            if raw_br == 'Auto':
                info_tmp = get_video_info(sanitized_f)
                target_quality_tag = f"{info_tmp.get('bitrate', 192)}k" if info_tmp else "192k"
            else:
                target_quality_tag = str(raw_br)
            log_entry = f"OP: AUDIO | {v_name} | Quality: {target_quality_tag}"
            already_done = False
            if os.path.exists(processed_log_path):
                with open(processed_log_path, 'r', encoding='utf-8') as pf:
                    if log_entry in pf.read(): already_done = True
            print(f" [{i}/{len(files)}] 🎵 Processing: {fname}".ljust(100))
            if global_config_mode and config_out_path:
                if not os.path.exists(config_out_path):
                    try: os.makedirs(config_out_path, exist_ok=True)
                    except: pass
                out_name = get_smart_filename(os.path.splitext(fname)[0], ".mp3", quality=target_quality_tag, op_tag=current_op_tag)
                final_out = os.path.join(config_out_path, out_name)
                final_out = ensure_unique_path(final_out, source_path=sanitized_f)
            elif local_save_mode:
                final_out = get_output_path(sanitized_f, v_dir, mode="local", quality=target_quality_tag, op_tag=current_op_tag)
            else:
                base_out = get_output_path(sanitized_f, root, mode="mirror", quality=target_quality_tag, op_tag=current_op_tag, do_clean_structure=do_clean_assets)
                if custom_folder:
                    parent = os.path.dirname(base_out)
                    final_folder = os.path.join(parent, custom_folder)
                    if not os.path.exists(final_folder): os.makedirs(final_folder, exist_ok=True)
                    final_out = os.path.join(final_folder, fname)
                else:
                    final_out = base_out
            final_out = os.path.splitext(final_out)[0] + ".mp3"
            final_out = ensure_unique_path(final_out, source_path=sanitized_f)
            info = get_video_info(sanitized_f)
            if info:
                source_br = info.get('bitrate', 0)
                target_br_str = "".join(filter(str.isdigit, str(target_quality_tag)))
                if target_br_str.isdigit():
                    target_br = int(target_br_str)
                    if source_br > 0:
                        if source_br < target_br and config.IGNORE_LOWER_QUALITY:
                            print(f" [{i}/{len(files)}] [REJECTED] Source bitrate ({source_br}k) < Target ({target_br}k): {fname}")
                            skipped += 1; skipped_list.append(f"{fname} (Low Bitrate: {source_br}k)"); continue
                        if source_br == target_br and config.IGNORE_EQUAL_QUALITY:
                            print(f" [{i}/{len(files)}] [REJECTED] Quality already matches ({source_br}k): {fname}")
                            skipped += 1; skipped_list.append(f"{fname} (Equal Bitrate)"); continue
            if already_done:
                print(f" [SKIP] Audio file already processed with same quality: {fname}")
                skipped += 1; skipped_list.append(fname); continue
            if trim_data and trim_data['mode'] == 'Random':
                info = get_video_info(sanitized_f)
                dur = info['dur'] if info else 120 
                max_start = max(0, dur - trim_data['duration'])
                trim_data['start'] = random.uniform(0, max_start)
                trim_data['end'] = trim_data['start'] + trim_data['duration']
            should_apply = is_sig_active and (mode == '1')
            plan = assemble_audio_command(sanitized_f, mode, s, trim_data, apply_signature=should_apply)
            cmd = []
            cmd.extend(plan["inputs"]) 
            if os.path.exists(CORE_POSTER):
                cmd.extend(["-i", CORE_POSTER])
                p_idx = cmd.count("-i") - 1
            else:
                p_idx = -1
            if plan["filter_complex"]:
                cmd.extend(["-filter_complex", plan["filter_complex"]])
                cmd.extend(["-map", plan["map"]])
            else:
                cmd.extend(["-map", "0:a?"])
            if p_idx != -1:
                cmd.extend(["-map", f"{p_idx}:v", "-c:v", "mjpeg", "-disposition:v:0", "attached_pic"])
            else:
                cmd.append("-vn")
            cmd.extend(plan["encoding_args"])
            cmd.extend(["-id3v2_version", "3", "-y", final_out])
            print(f" [>] Executing FFmpeg...")
            if run_ffmpeg(cmd, cpu_priority=config.CPU_PRIORITY, output_to_cleanup=final_out):
                success += 1
                if config.GLOBAL_AUTO_METADATA:
                    apply_instant_metadata(final_out, config.CORE_POSTER_PATH)
                with open(processed_log_path, 'a', encoding='utf-8') as pf:
                    pf.write(f"{log_entry} -> {final_out} [{time.strftime('%Y-%m-%d %H:%M')}]\n")
            else:
                print(f"\n [!] CRITICAL: Extraction failed for '{fname}'")
                ans = input("\n [WAIT] Review error, Press Enter to continue or [B] to stop: ").strip().upper()
                if ans == 'B': break
        except:
            traceback.print_exc()
            ans = smart_input("\n [ERROR] Press Enter to continue or [B] to stop: ").upper()
            if ans == 'B' or ans == '__BACK__': break
    t_total = time.time() - t_start
    op_names = {
        '1': "FULL PRODUCTION", '2': "CONVERT/TRANSCODE", 
        '3': "SMART CLIP", '4': "METADATA ONLY"
    }
    current_op = op_names.get(mode, "AUDIO PRODUCTION")
    if config.FINISH_SOUND_ALERT:
        try:
            import winsound
            winsound.Beep(1000, 600)
        except: pass
    clear_screen()
    print_header(current_op, "FINAL REPORT")
    print(f"  [+] Success     : {success}")
    print(f"  [>] Skipped     : {skipped}")
    print(f"  [-] Failed      : {len(files)-success-skipped}")
    print(f"  [@] Total Time  : {int(t_total//60)}m {int(t_total%60)}s")
    if skipped_list:
        print("-" * 40)
        print("  [SKIPPED FILES]:")
        for sk in skipped_list[:10]: print(f"   - {sk}")
    input("\n ► Press Enter to return to Menu...")
def audio_main_entry(files, root, force_local=False, is_folder_mode=False):
    print_header("AUDIO HUB", "MANUAL RECEPTION")
    if not files:
        p = input("\n ► Drag Folder or Media file (Audio/Video) here: ").strip().replace('"', '')
        if not p: return
        from utils import parse_dropped_paths
        raw_paths = parse_dropped_paths(p)
        files = find_media(raw_paths)
        root = raw_paths[0] if os.path.isdir(raw_paths[0]) else os.path.dirname(raw_paths[0])
    if not files:
        print("\n [!] No media files found."); time.sleep(1); return
    while True:
        choice = audio_reception_menu(len(files))
        if not choice: continue
        if (":" in choice or "\\" in choice or "/" in choice) and len(choice) > 5:
            from utils import parse_dropped_paths
            new_paths = parse_dropped_paths(choice)
            new_media = find_media(new_paths)
            new_audios = [f for f in new_media if f.lower().endswith(AUDIO_EXTS)]
            if new_audios:
                print("\n" + "!"*45)
                print(f" [?] PREVIOUS RECORD DETECTED ({len(files)} files)")
                print("  Y ➔ Remove old record and start new (Replace)")
                print("  N ➔ Add new files to current record (Append)")
                ans = input("\n ► Clear previous record? (Y/N) [Y]: ").strip().upper() or 'Y'
                if ans == 'Y':
                    files = new_audios
                    root = new_paths[0] if os.path.isdir(new_paths[0]) else os.path.dirname(new_paths[0])
                    print(f"\n [✓] Record cleared. Loaded {len(new_audios)} new files.")
                else:
                    files.extend(new_audios)
                    try:
                        all_dirs = [os.path.dirname(f) for f in files]
                        root = os.path.commonpath(all_dirs)
                    except: pass
                    print(f"\n [✓] Appended {len(new_audios)} files. Total now: {len(files)}")
                time.sleep(1)
            continue
        if choice == 'B': break
        if choice in ['1', '2', '3', '4']:
            run_audio_batch(files, root, choice, force_local=force_local, is_folder_mode=is_folder_mode)