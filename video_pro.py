import os
import sys
import traceback
import time
try:
    import msvcrt
except ImportError:
    msvcrt = None
from utils import (find_media, get_output_path, run_ffmpeg, get_video_info, 
                   prepare_file_for_processing, timestamp_to_seconds, get_smart_filename, 
                   log_event, parse_dropped_paths, extract_segments_as_clips, 
                   get_binary_path, ensure_unique_path, clear_screen, print_header, 
                   smart_input, VIDEO_EXTS, AUDIO_EXTS)
from censor_ui import get_batch_censor_config, get_individual_censor_config
from settings_manager import load_all_settings
from metadata import apply_instant_metadata
from video_logic import assemble_video_command
from config import *
import config
def video_reception_ui(file_count):
    print_header("VIDEO HUB", f"{file_count} FILES READY")
    print(" 1] » FULL SYSTEM          (Logo + Censor + Quality + Metadata)")
    print(" 2] » EDIT ONLY            (Logo + Layers + Metadata)")
    print(" 3] » CENSOR ONLY + META   (Freeze / Cut / Blur)")
    print(" 4] » METADATA ONLY        (Instant Metadata Sweep)")
    print(" 5] » QUALITY + META       (Change Quality + Metadata)")
    print(" 6] » QUALITY ONLY         (Change Resolution Only)")
    print(" 7] » EXTRACT AUDIO        (Convert Video to MP3/Audio)")
    print("-" * 70)
    print(" [💡] Tip: You can DRAG & DROP more files here to add them!")
    print(" [B] » BACK TO HUB")
    print("-" * 70)
    ans = smart_input(" ► Select Operation [1-7] or Drop Files: ")
    return 'B' if ans == '__BACK__' else ans
def run_video_production(files, root, mode, force_local=False, force_subfolder=False, is_folder_mode=False):
    from utils import launch_cpu_monitor
    launch_cpu_monitor()
    op_names = {
        '1': "FULL SYSTEM", '2': "EDIT ONLY", '3': "CENSOR ONLY", 
        '4': "METADATA ONLY", '5': "QUALITY + META", '6': "QUALITY ONLY", '7': "EXTRACT AUDIO"
    }
    current_op = op_names.get(mode, "VIDEO PRODUCTION")
    if mode == '4':
        print_header("VIDEO HUB", "METADATA SWEEP")
        ans = smart_input("\n ► Clean names? (Y/N) [Y]: ").upper() or 'Y'
        if ans == '__BACK__': return
        do_clean = (ans == 'Y')
        print(f"\n [🏷️] Processing {len(files)} videos...")
        success, failed = 0, 0
        t_start = time.time()
        for i, video in enumerate(files, 1):
            try:
                if apply_instant_metadata(video, config.CORE_POSTER_PATH):
                    success += 1
                else: failed += 1
                prepare_file_for_processing(video, is_metadata_only=True, do_clean=do_clean)
                print(f" [{i}/{len(files)}] Done: {os.path.basename(video)} ".ljust(100), end="\r")
            except: failed += 1
        t_total = time.time() - t_start
        if config.FINISH_SOUND_ALERT:
            try:
                import winsound
                winsound.Beep(1000, 400)
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
    if mode == '7':
        s = {'card_name': 'Auto-Extraction', 'target_q': 'Auto'}
    elif mode == '4':
        s = {'card_name': 'Metadata-Only', 'target_q': 'Original'}
    else:
        cards = {k: v for k, v in presets.items() if v.get('card_type', 'Video Card') == "Video Card"}
        title = "VIDEO PRODUCTION"
    if mode in ['7', '4']:
        pass
    elif mode == '3':
        s = {
            'card_name': "Censor Mode",
            'target_q': "Original",
            'bitrate': "Original",
            'fps': "Original",
            'logo_pos_str': "None",
            'logo_bounce_seq': ""
        }
    else:
        names = list(cards.keys())
        if not names: 
            print(f"\n [!] No relevant Settings Cards Found for {title}. Please create a card first."); time.sleep(1); return
        print(f"\n [■] Select Settings Card for {title}:")
        for i, n in enumerate(names, 1): print(f"  {i} ➔ {n}")
        print("  B ➔ [BACK]")
        idx = smart_input("\n ► Selection (Number or B): ").upper()
        if idx == 'B' or idx == '__BACK__': return
        try: s = cards[names[int(idx)-1]]
        except: return
        test_info = get_video_info(files[0])
        if test_info and mode != '7': 
            print("\n" + "-"*45)
            print(f" [!] Original Video Specifications (For Reference):")
            print(f"  • Source Quality  : {test_info['w']}x{test_info['h']}")
            print(f"  • Current Bitrate : {test_info['bitrate']} kbps")
            print(f"  • Current FPS     : {int(test_info['fps'])} fps")
            print("-" * 45)
            print(f"\n [⚙] Settings to be Applied (Card: {s.get('card_name','Current')}):")
            print(f"  ➔ Resolution : {s.get('target_q', config.DEFAULT_RESOLUTION)}")
            print(f"  ➔ Bitrate    : {s.get('bitrate', config.DEFAULT_BITRATE)}")
            print(f"  ➔ FPS        : {s.get('fps', str(config.DEFAULT_FPS))}")
            if mode in ['1', '2']:
                if s.get('logo_pos_str') == 'Dynamic-Bounce':
                    print(f"  ➔ Logo Move  : Dynamic ({s.get('logo_bounce_seq', 'Default: 4 corners')})")
                else:
                    print(f"  ➔ Logo Pos   : {s.get('logo_pos_str', 'Top-Right')}")
            mod_ans = smart_input("\n ► Use these settings? [Y: Yes] [N: Manual] [B: Back]: ").upper() or 'Y'
            if mod_ans == 'B' or mod_ans == '__BACK__': return
            if mod_ans == 'N':
                print("\n [!] Manual adjustments for this session:")
                v = smart_input(f" ► Res [{s.get('target_q', config.DEFAULT_RESOLUTION)}]: ")
                if v == '__BACK__': return
                s['target_q'] = v or s.get('target_q', config.DEFAULT_RESOLUTION)
                
                v = smart_input(f" ► FPS [{s.get('fps', str(config.DEFAULT_FPS))}]: ")
                if v == '__BACK__': return
                s['fps'] = v or s.get('fps', str(config.DEFAULT_FPS))
                
                v = smart_input(f" ► Bitrate [{s.get('bitrate', config.DEFAULT_BITRATE)}]: ")
                if v == '__BACK__': return
                if v.isdigit(): v += "k"
                s['bitrate'] = v or s.get('bitrate', config.DEFAULT_BITRATE)
    print_header(current_op, "SAVE STRATEGY")
    save_choice = "1"
    config_out_path = config.AUDIO_OUTPUT_PATH if mode == '7' else config.VIDEO_OUTPUT_PATH
    if not force_local and not force_subfolder:
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
        if force_local: save_choice = "2"
        else: save_choice = "1"
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
            print("  It seems the source has subfolders or extra files (images, etc.).")
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
                out_root = os.path.join(config_out_path if global_config_mode else root, "SGAM_STMEDIA_Output")
                from utils import clone_structure
                clone_structure(root, out_root, do_clean=do_clean_assets) 
    global_censor = None
    if mode in ['1', '3']:
        title_c = "Censor Content Processor" if mode == '1' else "Censor Mode Workflow"
        print_header(current_op, title_c.upper())
        print(f"\n [✂] {title_c}:")
        print("  1 ➔ Individual Mode: (Question per video)")
        print("  2 ➔ Batch Mode:      (One timing for all)")
        if mode == '1': print("  3 ➔ Skip Censoring")
        print("  B ➔ [BACK]")
        c_ans = smart_input("\n ► Your Choice [1]: ").upper() or "1"
        if c_ans == 'B' or c_ans == '__BACK__': return
        if c_ans == '2':
            config_c = get_batch_censor_config()
            if config_c == "BACK": return
            global_censor = config_c
        elif c_ans == '3' and mode == '1': 
            global_censor = "SKIP"
            
    success, skipped, failed = 0, 0, 0
    skipped_list = []
    redo_choice = None
    t_start = time.time()
    log_file_name = "sg_processed.txt"
    for i, video in enumerate(files, 1):
        if msvcrt and msvcrt.kbhit():
            if msvcrt.getch().upper() == b'B':
                print("\n [!] Batch cancelled by user.")
                break
        fname = os.path.basename(video)
        final_out = ""
        try:
            current_op_tag = ""
            if mode == '3': 
                current_op_tag = "CENSOR" 
            sanitized_video = prepare_file_for_processing(video, op_tag=current_op_tag)
            v_dir = os.path.dirname(sanitized_video)
            v_name = os.path.basename(sanitized_video)
            fname = v_name
            processed_log_path = os.path.join(v_dir, log_file_name)
            if mode == '7':
                info_tmp = get_video_info(sanitized_video)
                target_quality_tag = f"{info_tmp.get('bitrate', 192)}k" if info_tmp else "192k"
            else:
                raw_q = str(s.get('target_q', DEFAULT_RESOLUTION))
                if raw_q.lower() == 'original':
                    info_tmp = get_video_info(sanitized_video)
                    target_quality_tag = f"{info_tmp['h']}p" if info_tmp and info_tmp.get('h') else ""
                else:
                    target_quality_tag = raw_q
            log_entry = f"OP: {mode} | {v_name} | Quality: {target_quality_tag}"
            already_done = False
            if os.path.exists(processed_log_path):
                with open(processed_log_path, 'r', encoding='utf-8') as pf:
                    if log_entry in pf.read(): already_done = True
            if already_done:
                if redo_choice is None:
                    print("\n" + "!"*40)
                    print(f" [!] DUPLICATE DETECTED: {fname}")
                    print(f" [?] This file was already processed with quality {target_quality_tag}.")
                    print("  1 ➔ Skip All Duplicates (Default)")
                    print("  2 ➔ Reprocess All (Redo)")
                    print("  3 ➔ Ask me again for each")
                    ans = smart_input("\n ► How to proceed? [1]: ")
                    if ans == "__BACK__": return
                    if ans == "2": redo_choice = "REDO"
                    elif ans == "3": redo_choice = "ASK"
                    else: redo_choice = "SKIP"
                current_action = redo_choice
                if current_action == "ASK":
                    ans = input(f" ► File {fname} exists. Redo? (Y/N) [N]: ").strip().upper() or "N"
                    current_action = "REDO" if ans == "Y" else "SKIP"
                if current_action == "SKIP":
                    print(f" [{i}/{len(files)}] [SKIP] Already processed: {fname}")
                    skipped += 1; skipped_list.append(fname); continue
                else:
                    print(f" [{i}/{len(files)}] [REDO] Reprocessing as requested: {fname}")
            proc_tag = current_op_tag
            if mode in ['1', '3']:
                if global_censor and global_censor != "SKIP":
                    if global_censor.get('mode') == 'CUT' and not global_censor.get('ivs'):
                        proc_tag = ""
                    else:
                        proc_tag = str(global_censor.get('mode', 'CENSOR')).upper()
            if local_save_mode:
                final_out = get_output_path(sanitized_video, v_dir, mode="local", quality=target_quality_tag, op_tag=proc_tag)
            elif global_config_mode and config_out_path:
                if not os.path.exists(config_out_path):
                    try: os.makedirs(config_out_path, exist_ok=True)
                    except: pass
                out_name = get_smart_filename(os.path.splitext(fname)[0], os.path.splitext(fname)[1], quality=target_quality_tag, op_tag=proc_tag)
                final_out = os.path.join(config_out_path, out_name)
                final_out = ensure_unique_path(final_out, source_path=sanitized_video)
            else:
                out_mode = s.get('out_mode_str', 'Mirror').lower()
                base_for_out = v_dir if force_subfolder else root
                final_out = get_output_path(sanitized_video, base_for_out, mode=out_mode, quality=target_quality_tag, op_tag=proc_tag, do_clean_structure=do_clean_assets)
                if mode != '7':
                    info = get_video_info(sanitized_video)
                    if info:
                        source_h = info['h']
                        target_q_str = str(s.get('target_q', config.DEFAULT_RESOLUTION)).replace('p', '')
                        if target_q_str.isdigit():
                            target_h = int(target_q_str)
                            if source_h < target_h and config.IGNORE_LOWER_QUALITY:
                                print(f" [{i}/{len(files)}] [REJECTED] Source resolution ({source_h}p) < Target ({target_h}p): {fname}")
                                skipped += 1; skipped_list.append(f"{fname} (Low Resolution)"); continue
                            if source_h == target_h and config.IGNORE_EQUAL_QUALITY:
                                print(f" [{i}/{len(files)}] [REJECTED] Resolution already matches ({source_h}p): {fname}")
                                skipped += 1; skipped_list.append(f"{fname} (Equal Resolution)"); continue
            print(f" [{i}/{len(files)}] » Processing: {fname}".ljust(100))
            censor_data = None
            if mode in ['1', '3']:
                if global_censor == "SKIP": censor_data = None
                elif global_censor: censor_data = global_censor
                else:
                    info = get_video_info(sanitized_video)
                    dur = info['dur'] if info else 0
                    config_c = get_individual_censor_config(sanitized_video, dur)
                    if config_c == "BACK": return
                    censor_data = config_c
                if mode == '3' and censor_data and censor_data != "SKIP":
                    if censor_data.get('mode') == 'CUT' and not censor_data.get('ivs'):
                        proc_tag = ""
                    else:
                        proc_tag = str(censor_data.get('mode', 'CENSOR')).upper()
                    if local_save_mode:
                        final_out = get_output_path(sanitized_video, v_dir, mode="local", quality=target_quality_tag, op_tag=proc_tag)
                    elif global_config_mode and config_out_path:
                        out_name = get_smart_filename(os.path.splitext(fname)[0], os.path.splitext(fname)[1], quality=target_quality_tag, op_tag=proc_tag)
                        final_out = os.path.join(config_out_path, out_name)
                        final_out = ensure_unique_path(final_out, source_path=sanitized_video)
                    else:
                        out_mode = s.get('out_mode_str', 'Mirror').lower()
                        base_for_out = v_dir if force_subfolder else root
                        final_out = get_output_path(sanitized_video, base_for_out, mode=out_mode, quality=target_quality_tag, op_tag=proc_tag, do_clean_structure=do_clean_assets)
            if mode == '7':
                info = get_video_info(sanitized_video)
                source_br = info.get('bitrate', 192) if info else 192
                bitrate_str = f"{source_br}k"
                base_name = os.path.splitext(fname)[0]
                if local_save_mode:
                    out_dir = v_dir
                elif global_config_mode and config.AUDIO_OUTPUT_PATH:
                    out_dir = config.AUDIO_OUTPUT_PATH
                    if not os.path.exists(out_dir): os.makedirs(out_dir, exist_ok=True)
                else:
                    out_dir = os.path.dirname(get_output_path(sanitized_video, root, mode="mirror"))
                final_out = os.path.join(out_dir, get_smart_filename(base_name, ".mp3", quality=bitrate_str))
                final_out = ensure_unique_path(final_out, source_path=sanitized_video)
                print(f" [>] Extracting Audio ({bitrate_str}) + Adding Watermark...")
                from audio_logic import assemble_audio_command
                audio_plan = assemble_audio_command(sanitized_video, '7', {'bitrate': bitrate_str}, apply_signature=False)
                cmd = audio_plan["inputs"]
                if audio_plan["filter_complex"]:
                    cmd.extend(["-filter_complex", audio_plan["filter_complex"]])
                    cmd.extend(["-map", audio_plan["map"]])
                else:
                    cmd.extend(["-map", "0:a?"])
                cmd.extend(audio_plan["encoding_args"])
                cmd.extend(["-y", final_out])
                if run_ffmpeg(cmd, cpu_priority=config.CPU_PRIORITY, output_to_cleanup=final_out):
                    success += 1
                    if config.GLOBAL_AUTO_METADATA:
                        apply_instant_metadata(final_out, config.CORE_POSTER_PATH)
                    with open(processed_log_path, 'a', encoding='utf-8') as pf:
                        pf.write(f"{v_name} -> {final_out} (SMART-EXTRACT-WITH-WP)\n")
                else: failed += 1
                continue
            plan = assemble_video_command(sanitized_video, mode, s, censor_data)
            if not plan: 
                print(f" [!] Failed to generate plan for: {fname}")
                failed += 1; continue
            cmd = plan["inputs"]
            if plan["filter_complex"]: cmd.extend(["-filter_complex", plan["filter_complex"]])
            cmd.extend(plan["encoding_args"])
            cmd.extend(["-map", plan["v_label"], "-map", f"{plan['a_label'] if plan['a_label'] !='[0:a]' else '0:a?'}"])
            if "poster" in plan["idx_map"]:
                cmd.extend(["-map", str(plan["idx_map"]["poster"]), "-c:v:1", "mjpeg", "-disposition:v:1", "attached_pic"])
            cmd.extend(["-y", final_out])
            if run_ffmpeg(cmd, cpu_priority=config.CPU_PRIORITY, output_to_cleanup=final_out):
                success += 1
                if config.GLOBAL_AUTO_METADATA:
                    apply_instant_metadata(final_out, config.CORE_POSTER_PATH)
                if censor_data and censor_data.get("save_cuts"):
                    extract_segments_as_clips(sanitized_video, censor_data["ivs"], v_dir)
                with open(processed_log_path, 'a', encoding='utf-8') as pf:
                    pf.write(f"{log_entry} -> {final_out} [{time.strftime('%Y-%m-%d %H:%M')}]\n")
            else: 
                failed += 1
                print(f"\n [✖] FFmpeg Execution Failed for: {fname}")
                log_event(f"FFmpeg Failure on {fname} | Command: {' '.join(cmd)}", level="ERROR")
                ans = input("\n ► Press Enter to see next file or [B] to Stop Batch: ").strip().upper()
                if ans == 'B': break
        except Exception as e:
            log_event(f"Python Exception on {fname}: {str(e)}", level="CRITICAL")
            print(f"\n [!] Python Error: {e}")
            failed += 1
            ans = input("\n ► Press Enter to continue or [B] to Stop Batch: ").strip().upper()
            if ans == 'B': break
    t_total = time.time() - t_start
    op_names = {
        '1': "FULL SYSTEM", '2': "EDIT ONLY", '3': "CENSOR ONLY", 
        '4': "METADATA ONLY", '5': "QUALITY + META", '6': "QUALITY ONLY", '7': "EXTRACT AUDIO"
    }
    current_op = op_names.get(mode, "PRODUCTION")
    if config.FINISH_SOUND_ALERT:
        try:
            import winsound
            winsound.Beep(1000, 600) 
        except: pass
    print_header(current_op, "FINAL REPORT")
    print(f"  [+] Success     : {success}")
    print(f"  [>] Skipped     : {skipped}")
    print(f"  [-] Failed      : {failed}")
    print(f"  [@] Total Time  : {int(t_total//60)}m {int(t_total%60)}s")
    if skipped_list:
        print("-" * 40)
        print("  [SKIPPED FILES]:")
        for sk in skipped_list[:10]: print(f"   - {sk}")
        if len(skipped_list) > 10: print(f"   ... and {len(skipped_list)-10} more.")
    print("="*70)
    input("\n ► Press Enter to return to Home...")
def video_main_entry(files, root, force_local=False, force_subfolder=False, is_folder_mode=False):
    print_header("VIDEO HUB", "MANUAL RECEPTION")
    if not files:
        p = input("\n ► Drag Folder or Video file here and press Enter: ").strip().replace('"', '')
        if not p: return
        raw_paths = parse_dropped_paths(p)
        files = find_media(raw_paths)
        files = [f for f in files if f.lower().endswith(VIDEO_EXTS)]
        root = raw_paths[0] if os.path.isdir(raw_paths[0]) else os.path.dirname(raw_paths[0])
    if not files:
        print("\n [!] No video files found in selection."); time.sleep(1); return
    while True:
        choice = video_reception_ui(len(files))
        if (":" in choice or "\\" in choice or "/" in choice) and len(choice) > 5:
            new_paths = parse_dropped_paths(choice)
            new_media = find_media(new_paths)
            new_videos = [f for f in new_media if f.lower().endswith(VIDEO_EXTS)]
            if new_videos:
                print("\n" + "!"*45)
                print(f" [?] PREVIOUS RECORD DETECTED ({len(files)} files)")
                print("  Y ➔ Remove old record and start new (Replace)")
                print("  N ➔ Add new files to current record (Append)")
                ans = smart_input("\n ► Clear record? (Y/N) [Y]: ").upper() or 'Y'
                if ans == '__BACK__': continue
                if ans == 'Y':
                    files = new_videos
                    root = new_paths[0] if os.path.isdir(new_paths[0]) else os.path.dirname(new_paths[0])
                    print(f"\n [✓] Record cleared. Loaded {len(new_videos)} new files.")
                else:
                    files.extend(new_videos)
                    try:
                        all_dirs = [os.path.dirname(f) for f in files]
                        root = os.path.commonpath(all_dirs)
                    except:
                        pass 
                    print(f"\n [✓] Appended {len(new_videos)} files. Total now: {len(files)}")
                time.sleep(1)
            continue
        choice = choice.upper()
        if choice == 'B': break
        if choice in '1234567':
            run_video_production(files, root, choice, force_local=force_local, force_subfolder=force_subfolder, is_folder_mode=is_folder_mode)