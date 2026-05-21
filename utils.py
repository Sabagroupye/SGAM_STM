import os
import subprocess
import json
import shutil
import re
import sys
import time
import shlex
VIDEO_EXTS = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.ts')
AUDIO_EXTS = ('.mp3', '.wav', '.m4a', '.flac', '.ogg', '.opus', '.aac', '.wma', '.mka')
COMPANY_NAME = "SABAGROUP"
def get_assets_dir():
    from config import CORE_ASSETS_DIR
    return CORE_ASSETS_DIR
def get_binary_path(name):
    assets_dir = get_assets_dir()
    ext = ".exe" if os.name == "nt" else ""
    local_path = os.path.join(assets_dir, f"{name}{ext}")
    if os.path.exists(local_path): return local_path
    try:
        import importlib
        sf = importlib.import_module("static_ffmpeg")
        if name == "ffmpeg": return sf.get_ffmpeg_bin()
        if name == "ffprobe": return sf.get_ffprobe_bin()
    except: pass
    return name 
def apply_cpu_priority():
    try:
        from config import CPU_PRIORITY
        import psutil
        p = psutil.Process(os.getpid())
        if CPU_PRIORITY == "Idle": p.nice(psutil.IDLE_PRIORITY_CLASS)
        elif CPU_PRIORITY == "BelowNormal": p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        elif CPU_PRIORITY == "Normal": p.nice(psutil.NORMAL_PRIORITY_CLASS)
        elif CPU_PRIORITY == "AboveNormal": p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
        elif CPU_PRIORITY == "High": p.nice(psutil.HIGH_PRIORITY_CLASS)
    except: pass
def timestamp_to_seconds(ts, duration=99999):
    try:
        p = str(ts).strip().split(':')
        if len(p) == 3: return int(p[0])*3600 + int(p[1])*60 + float(p[2])
        if len(p) == 2: return int(p[0])*60 + float(p[1])
        return min(float(ts), duration)
    except: return 0.0
def parse_dropped_paths(p_in):
    if not p_in: return []
    p_in = p_in.strip()
    try:
        if '"' in p_in:
            import shlex
            return shlex.split(p_in)
        elif ' ' in p_in:
            paths = re.split(r'\s+(?=[a-zA-Z]:\\)', p_in)
            return [p.strip() for p in paths if p.strip()]
        else:
            return [p_in]
    except:
        return [p.strip().replace('"', '') for p in p_in.split('" "') if p.strip()]
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
clear = clear_screen

def smart_input(prompt):
    val = input(prompt).strip()
    if val.upper() == 'B':
        return "__BACK__"
    return val
def get_choice(prompt, options, default="1"):
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1): print(f"  {i}) {opt}")
    c = smart_input(f" Choice (1-{len(options)}) [{default}]: ") or default
    if c == "__BACK__": return "B"
    try:
        if c.isdigit(): return options[int(c)-1]
        return c
    except: return options[0]
def print_header(main_op="SGAM STMEDIA", sub_op=None):
    clear_screen()
    print("=" * 75)
    print(f"  SGAM STM | @SABAGROUPYE | +967 770574579 | STMEDIA ENGINE 2026.05 ")
    print("=" * 75)
    if sub_op:
        print(f"  [ {main_op} ] » {sub_op}")
    else:
        print(f"  [ {main_op} ]")
    print("-" * 75)
def find_media(paths):
    media_files = []
    all_exts = VIDEO_EXTS + AUDIO_EXTS
    for p in paths:
        if os.path.isfile(p) and p.lower().endswith(all_exts):
            media_files.append(p)
        elif os.path.isdir(p):
            for root, _, files in os.walk(p):
                if "SGAM_Stmedia_Output" in root: continue
                for f in files:
                    if f.lower().endswith(all_exts):
                        media_files.append(os.path.join(root, f))
    return media_files
def sanitize_name(name):
    from config import REMOVE_WORDS, REMOVE_SYMBOLS
    from tag_logic import get_system_tag, ensure_safe_filename
    base, ext = os.path.splitext(name)
    mandatory = get_system_tag() 
    placeholder = "___SGAM_LOCK___"
    protected_base = base.replace(mandatory, placeholder)
    sorted_words = sorted([w for w in REMOVE_WORDS if w.strip()], key=len, reverse=True)
    for word in sorted_words:
        if word.lower() in mandatory.lower(): continue
        protected_base = re.sub(re.escape(word), '', protected_base, flags=re.IGNORECASE)
    for sym in REMOVE_SYMBOLS:
        if sym in mandatory: continue
        protected_base = protected_base.replace(sym, ' ') 
    protected_base = re.sub(r'\s+', ' ', protected_base) 
    protected_base = re.sub(r'[ _\-\.]{2,}', '_', protected_base) 
    final_base = protected_base.replace(placeholder, mandatory).strip(' _-.')
    return ensure_safe_filename(f"{final_base}{ext}")
def prepare_file_for_processing(file_path, is_metadata_only=False, do_clean=True, op_tag=""):
    from config import RENAME_ORIGINAL_ON_ALL
    dir_name = os.path.dirname(file_path)
    old_name = os.path.basename(file_path)
    if RENAME_ORIGINAL_ON_ALL or is_metadata_only:
        if is_metadata_only:
            quality_tag = None
            try:
                info = get_video_info(file_path)
                if info:
                    if file_path.lower().endswith(('.mp3', '.wav', '.m4a', '.flac')):
                        quality_tag = f"{info['bitrate']}k"
                    else:
                        quality_tag = f"{info['h']}p"
            except: pass
            base_name = os.path.splitext(old_name)[0]
            ext = os.path.splitext(old_name)[1]
            is_folder = os.path.isdir(file_path)
            new_name = get_smart_filename(base_name, ext, quality=quality_tag, do_clean=do_clean, is_folder=is_folder)
        else:
            if do_clean:
                new_name = sanitize_name(old_name)
            else:
                from tag_logic import ensure_safe_filename
                new_name = ensure_safe_filename(old_name)
        if old_name != new_name:
            new_path = os.path.join(dir_name, new_name)
            try:
                new_path = ensure_unique_path(new_path, source_path=file_path)
                os.rename(file_path, new_path)
                return new_path
            except: return file_path
    return file_path
def log_event(message, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(base_path, "sgam_process_log.txt")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
    except Exception as e:
        print(f" LOG ERROR: {e}")

def launch_cpu_monitor():
    import config
    if not getattr(config, 'AUTO_OPEN_CPU_MONITOR', False): return
    try:
        import psutil
        import subprocess
        is_running = False
        for p in psutil.process_iter(['cmdline']):
            try:
                cmd = p.info.get('cmdline')
                if isinstance(cmd, list) and any('cpu_controller.py' in str(arg) for arg in cmd):
                    is_running = True; break
            except: pass
        if not is_running:
            script_path = os.path.join(os.path.dirname(__file__), "cpu_controller.py")
            if os.path.exists(script_path):
                if os.name == 'nt':
                    subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                elif sys.platform == 'darwin':  # macOS
                    cmd_mac = f'tell application "Terminal" to do script "\'{sys.executable}\' \'{script_path}\'"'
                    subprocess.Popen(['osascript', '-e', cmd_mac])
                else:  # Linux
                    import shutil
                    terminal_launched = False
                    for term in ['gnome-terminal', 'konsole', 'xfce4-terminal', 'xterm']:
                        if shutil.which(term):
                            if term == 'gnome-terminal':
                                subprocess.Popen([term, '--', sys.executable, script_path])
                            elif term == 'xterm':
                                subprocess.Popen([term, '-e', sys.executable, script_path])
                            else:
                                subprocess.Popen([term, '-e', f'"{sys.executable}" "{script_path}"'])
                            terminal_launched = True
                            break
                    if not terminal_launched:
                        subprocess.Popen([sys.executable, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except: pass
def run_ffmpeg(args, cpu_priority="Normal", output_to_cleanup=None):
    ff_path = get_binary_path("ffmpeg")
    if args and args[0] == "ffmpeg": args[0] = ff_path
    full_cmd = " ".join([f'"{a}"' if ' ' in a else a for a in args])
    log_event(f"EXECUTING: {full_cmd}")
    base_path = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(base_path, "sgam_process_log.txt")
    print(f"\n [🎬] Processing... (Log: {os.path.basename(log_file)})")
    process = None
    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                   text=True, encoding='utf-8', errors='ignore', cwd=get_assets_dir())
        try:
            import psutil
            p = psutil.Process(process.pid)
            if cpu_priority == "Idle": p.nice(psutil.IDLE_PRIORITY_CLASS)
            elif cpu_priority == "BelowNormal": p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            elif cpu_priority == "Normal": p.nice(psutil.NORMAL_PRIORITY_CLASS)
            elif cpu_priority == "AboveNormal": p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
            elif cpu_priority == "High": p.nice(psutil.HIGH_PRIORITY_CLASS)
        except: pass
        all_output = []
        with open(log_file, "a", encoding="utf-8") as lf:
            lf.write(f"\n--- SESSION START: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            lf.write(f"COMMAND: {full_cmd}\n\n")
            for line in process.stdout:
                lf.write(line)
                lf.flush()
                all_output.append(line.strip())
                if "time=" in line:
                    time_match = re.search(r'time=([\d:.]+)', line)
                    if time_match:
                        print(f"  ➔ Progress Time: {time_match.group(1)}".ljust(80), end='\r')
        process.wait()
        print("\n [✓] Finished.")
        if process.returncode != 0:
            print("\n" + "!"*50)
            print(" [!] ERROR: FFmpeg execution failed!")
            if output_to_cleanup and os.path.exists(output_to_cleanup):
                try: os.remove(output_to_cleanup); print(f" [!] Partial output deleted: {os.path.basename(output_to_cleanup)}")
                except: pass
            return False
        return True
    except KeyboardInterrupt:
        print("\n\n [!] STOPPED BY USER (KeyboardInterrupt)")
        if process:
            process.kill()
            process.wait()
        if output_to_cleanup and os.path.exists(output_to_cleanup):
            try: os.remove(output_to_cleanup); print(f" [!] Cancelled: Partial output deleted.")
            except: pass
        sys.exit(1)
    except Exception as e:
        log_event(f"CRITICAL ERROR: {str(e)}", level="CRITICAL")
        print(f" [!] System Error: {e}")
        if output_to_cleanup and os.path.exists(output_to_cleanup):
            try: os.remove(output_to_cleanup); print(f" [!] Error: Partial output deleted.")
            except: pass
        return False
def get_video_info(path):
    fp_path = get_binary_path("ffprobe")
    try:
        cmd = [fp_path, "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", path]
        res = subprocess.check_output(cmd).decode('utf-8')
        data = json.loads(res)
        fmt = data.get('format', {})
        v_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'video'), {})
        a_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'audio'), None)
        return {
            'dur': float(fmt.get('duration', 0)),
            'bitrate': int(fmt.get('bit_rate', 0)) // 1000,
            'w': int(v_stream.get('width', 0)),
            'h': int(v_stream.get('height', 0)),
            'fps': eval(v_stream.get('r_frame_rate', '25/1')),
            'has_audio': a_stream is not None
        }
    except: return None
def verify_signature_image(path, expected_w=3189, expected_h=1417):
    if not os.path.exists(path): return False
    try:
        from PIL import Image
        with Image.open(path) as img:
            if img.width != expected_w or img.height != expected_h:
                return False
            img = img.convert("RGBA")
            data = img.getdata()
            for item in data:
                if item[3] > 0:
                    if item[0] != 255 or item[1] != 255 or item[2] != 255:
                        return False
            return True
    except: return False
def get_smart_filename(original_name, ext, quality=None, do_clean=True, extra_tag="", is_folder=False, op_tag=""):
    from config import FILE_SUFFIX
    from tag_logic import structure_smart_filename, clean_quality_redundancy, ensure_safe_filename
    if do_clean:
        cleaned_base = sanitize_name(original_name).replace(os.path.splitext(original_name)[1], '')
    else:
        cleaned_base = ensure_safe_filename(original_name).replace(os.path.splitext(original_name)[1], '')
    cleaned_base = clean_quality_redundancy(cleaned_base, quality)
    if extra_tag:
        cleaned_base = f"{cleaned_base.strip()} {extra_tag}"
    return structure_smart_filename(cleaned_base, FILE_SUFFIX, quality, ext, is_folder=is_folder, do_clean=do_clean, op_tag=op_tag)
def ensure_unique_path(target_path, source_path=None):
    import os
    import re
    from config import NAME_SEPARATOR
    needs_versioning = False
    if source_path and target_path.lower() == source_path.lower():
        needs_versioning = True
    elif os.path.exists(target_path):
        needs_versioning = True
    if not needs_versioning:
        return target_path
    dir_name = os.path.dirname(target_path)
    base_name, ext = os.path.splitext(os.path.basename(target_path))
    version_pattern = rf"{re.escape(NAME_SEPARATOR)}(\d+)$"
    match = re.search(version_pattern, base_name)
    if match:
        version = int(match.group(1)) + 1
        clean_base = base_name[:match.start()]
    else:
        version = 0
        clean_base = base_name
    while True:
        new_name = f"{clean_base}{NAME_SEPARATOR}{version}{ext}"
        new_path = os.path.join(dir_name, new_name)
        collision = False
        if source_path and new_path.lower() == source_path.lower():
            collision = True
        elif os.path.exists(new_path):
            collision = True
        if not collision:
            return new_path
        version += 1
def get_output_path(video_path, base_dir, mode="mirror", quality=None, op_tag="", do_clean_structure=False):
    input_dir = os.path.dirname(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    ext = os.path.splitext(os.path.basename(video_path))[1]
    final_name = get_smart_filename(base_name, ext, quality, op_tag=op_tag)
    potential_path = os.path.join(input_dir, final_name)
    potential_path = ensure_unique_path(potential_path, source_path=video_path)
    final_name = os.path.basename(potential_path)
    if mode == "local":
        return os.path.join(input_dir, final_name)
    
    # Detect if base_dir is equal to the batch/script directory (launcher directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    is_batch_dir = False
    if base_dir:
        try:
            is_batch_dir = os.path.abspath(base_dir).lower() == os.path.abspath(script_dir).lower()
        except: pass

    # Check if base_dir is actually a parent of input_dir
    is_parent = False
    if base_dir and not is_batch_dir:
        try:
            abs_base = os.path.abspath(base_dir).lower() + os.sep
            abs_input = os.path.abspath(input_dir).lower() + os.sep
            is_parent = abs_input.startswith(abs_base)
        except: pass

    if not base_dir or is_batch_dir or not is_parent:
        # If files were dragged from multiple paths or base_dir is the launcher folder,
        # we create the output folder next to each individual file.
        out_root = os.path.join(input_dir, "SGAM_STMEDIA_Output")
        rel_path = ""
    else:
        out_root = os.path.join(base_dir, "SGAM_STMEDIA_Output")
        try:
            if os.name == 'nt':
                if os.path.splitdrive(input_dir)[0].lower() != os.path.splitdrive(base_dir)[0].lower():
                    rel_path = ""
                else:
                    rel_path = os.path.relpath(input_dir, base_dir)
                    if rel_path.startswith(".."): rel_path = ""
            else:
                rel_path = os.path.relpath(input_dir, base_dir)
                if rel_path.startswith(".."): rel_path = ""
            if rel_path == "." or rel_path.startswith(".."): rel_path = ""
            if rel_path and do_clean_structure:
                path_segments = rel_path.split(os.sep)
                clean_segments = [sanitize_name(seg) for seg in path_segments]
                rel_path = os.path.join(*clean_segments)
        except:
            rel_path = ""

    if not os.path.exists(out_root): os.makedirs(out_root, exist_ok=True)
    final_dir = os.path.join(out_root, rel_path)
    if not os.path.exists(final_dir): os.makedirs(final_dir, exist_ok=True)
    final_path = os.path.join(final_dir, final_name)
    return ensure_unique_path(final_path, source_path=video_path)
def clone_structure(src_root, dst_root, do_clean=True):
    exts = VIDEO_EXTS + AUDIO_EXTS
    import shutil
    for root, dirs, files in os.walk(src_root):
        if "SGAM_STMEDIA_Output" in root: continue
        rel = os.path.relpath(root, src_root)
        if rel != ".":
            segs = rel.split(os.sep)
            clean_segs = [sanitize_name(s) if do_clean else s for s in segs]
            rel_clean = os.path.join(*clean_segs)
        else:
            rel_clean = ""
        dest_folder = os.path.join(dst_root, rel_clean)
        if not os.path.exists(dest_folder): os.makedirs(dest_folder, exist_ok=True)
        for f in files:
            if not f.lower().endswith(exts):
                src_file = os.path.join(root, f)
                new_f_name = sanitize_name(f) if do_clean else f
                dst_file = os.path.join(dest_folder, new_f_name)
                try:
                    if not os.path.exists(dst_file): shutil.copy2(src_file, dst_file)
                except: pass
def extract_segments_as_clips(video_path, intervals, output_dir):
    import subprocess
    from config import GLOBAL_CLIPS_OUTPUT_PATH
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    target_subfolder = "SGAM_CUTS_VIDEO"
    if GLOBAL_CLIPS_OUTPUT_PATH:
        clips_dir = os.path.join(GLOBAL_CLIPS_OUTPUT_PATH, target_subfolder)
    else:
        clips_dir = os.path.join(output_dir, target_subfolder)
    try:
        if not os.path.exists(clips_dir):
            os.makedirs(clips_dir, exist_ok=True)
    except:
        clips_dir = os.path.join(output_dir, target_subfolder)
        os.makedirs(clips_dir, exist_ok=True)
    for i, (s, e) in enumerate(intervals, 1):
        dur = e - s
        if dur <= 0: continue
        out_clip = os.path.join(clips_dir, f"{base_name}_cut_{i}.mp4")
        cmd = ["ffmpeg", "-ss", str(s), "-t", str(dur), "-i", video_path, "-c", "copy", "-y", out_clip]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except: pass