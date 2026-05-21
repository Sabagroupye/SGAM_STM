import os
import sys
import time
import json
import re
import config as cfg
from utils import clear_screen, get_smart_filename, smart_input
from metadata import apply_instant_metadata, get_fast_info
from internal_paths import FFMPEG_FOLDER
try:
    import yt_dlp
except ImportError:
    print("\n [!] 'yt-dlp' library not found. Please run 'launcher.py' first.")
    sys.exit()
QUEUE_FILE = "youtube_queue.json"
def is_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"
    return re.match(pattern, url)
def load_queue():
    if os.path.exists(QUEUE_FILE):
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {"pending": [], "completed": []}
    return {"pending": [], "completed": []}
def save_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=4, ensure_ascii=False)
def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%')
        s = d.get('_speed_str', 'N/A')
        t = d.get('_eta_str', 'N/A')
        print(f"  ➔ Downloading: {p} | Speed: {s} | ETA: {t}".ljust(80), end='\r')
    elif d['status'] == 'finished':
        print(f"\n [✓] Finished. Finalizing...")
def get_formats_and_info(url):
    print(f"\n [⏳] Analysis in progress... {url[:40]}...")
    ydl_opts = {
        'quiet': True, 'no_warnings': True, 'nocheckcertificate': True,
        'extract_flat': False
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('formats', []), info.get('title', 'Unknown')
    except: return None, None
def download_youtube_video():
    while True:
        clear_screen()
        queue = load_queue()
        from utils import print_header
        print_header("YOUTUBE PRO", "DOWNLOADER HUB")
        print(f"\n [!] PENDING TASKS: {len(queue['pending'])}")
        print(" [R] Resume | [C] Clear Queue | [B] Back")
        print("\n [ADD] Paste YouTube URL (Multiple: use space or comma)")
        print(" [B] Back to Hub")
        raw_in = smart_input("\n ► URL / Action: ")
        if not raw_in: continue
        if raw_in == '__BACK__': return 
        if raw_in.upper() == 'B': return 
        if raw_in.upper() == 'R' and queue["pending"]:
            process_queue(queue)
            continue
        if raw_in.upper() == 'C':
            queue["pending"] = []
            save_queue(queue)
            print(" [✓] Queue cleared."); time.sleep(1); continue
        new_urls = [u.strip() for u in raw_in.replace(',', ' ').split() if is_youtube_url(u.strip())]
        custom_name = None
        if len(new_urls) == 1 and cfg.YOUTUBE_SMART_NAMING:
            print(f"\n [💎] Single Link Detected.")
            custom_name = smart_input(" ► Enter Custom Filename (Optional): ")
            if custom_name == '__BACK__': continue
            if not custom_name: custom_name = None
        if not new_urls:
            if not is_youtube_url(raw_in) and raw_in.upper() not in ['R', 'C', 'B']:
                print("\n [✖] Invalid YouTube Link Detected. Ignoring..."); time.sleep(1.5)
            continue
        for u in new_urls:
            if u not in [item['url'] for item in queue["pending"]]:
                queue["pending"].append({"url": u, "status": "pending", "custom_name": custom_name})
        save_queue(queue)
        print(f" [✓] Added {len(new_urls)} links to queue.")
        process_queue(queue)
def process_queue(queue):
    success, failed = 0, 0
    t_start = time.time()
    while queue["pending"]:
        item = queue["pending"][0]
        url = item["url"]
        user_filename = item.get("custom_name")
        clear_screen()
        print(f"\n {'='*10} PROCESSING TASK {'='*10}")
        formats, title = get_formats_and_info(url)
        if not formats:
            print(f" [✖] Could not fetch info for: {url}. Skipping...")
            queue["pending"].pop(0)
            save_queue(queue)
            time.sleep(2); continue
        target_title = user_filename if user_filename else title
        print(f" [🎬] TARGET: {target_title}")
        print("-" * 50)
        print(" 1) Video + Audio (MP4/MKV)")
        print(" 2) Audio Only (MP3)")
        print(" B) [ BACK ]")
        mode = smart_input("\n ► Selection [1]: ") or "1"
        if mode == '__BACK__' or mode.upper() == 'B': return 
        if mode.upper() == 'B': return 
        fmt_id = "bestvideo+bestaudio/best"
        ext_choice = "mp4"
        selected_quality = "Best"
        if mode == "1":
            print("\n Available Qualities:")
            v_list = []
            seen = set()
            for f in formats:
                res = f.get('resolution')
                ext = f.get('ext')
                if res and res != 'audio only' and ext in ['mp4', 'webm']:
                    label = f"{res} ({ext})"
                    if label not in seen:
                        v_list.append({'id': f['format_id'], 'lbl': label, 'res_only': res})
                        seen.add(label)
            for i, v in enumerate(v_list, 1):
                print(f"  {i}) {v['lbl']}")
            print("  B) [ BACK ]")
            c = smart_input(f"\n ► Select (1-{len(v_list)}) [Best]: ").upper()
            if c == '__BACK__' or c == 'B': return
            if c.isdigit() and 1 <= int(c) <= len(v_list):
                fmt_id = f"{v_list[int(c)-1]['id']}+bestaudio/best"
                selected_quality = v_list[int(c)-1]['res_only']
        else:
            ext_choice = "mp3"
            print("\n Available Audio Qualities:")
            a_list = []
            for f in formats:
                if f.get('vcodec') == 'none' and f.get('abr'):
                    label = f"{f['abr']}kbps"
                    a_list.append({'id': f['format_id'], 'lbl': label})
            a_list.sort(key=lambda x: float(x['lbl'].replace('kbps','')), reverse=True)
            for i, a in enumerate(a_list, 1): print(f"  {i}) {a['lbl']}")
            print("  B) [ BACK ]")
            c = smart_input(f"\n ► Select [Best]: ").upper()
            if c == '__BACK__' or c == 'B': return
            if c.isdigit() and 1 <= int(c) <= len(a_list): 
                fmt_id = a_list[int(c)-1]['id']
                selected_quality = a_list[int(c)-1]['lbl']
        final_ext = f".{ext_choice}"
        smart_name = get_smart_filename(target_title, final_ext, quality=selected_quality)
        out_dir = os.path.join(cfg.YOUTUBE_DOWNLOAD_PATH, "SGAM_YT_Video" if mode=="1" else "SGAM_YT_Audio")
        if not os.path.exists(out_dir): os.makedirs(out_dir, exist_ok=True)
        final_path = os.path.join(out_dir, smart_name)
        print(f"\n [🚀] Downloading to: {smart_name}...")
        ydl_opts = {
            'format': fmt_id,
            'outtmpl': final_path,
            'ffmpeg_location': FFMPEG_FOLDER,
            'progress_hooks': [progress_hook],
            'quiet': True, 'no_warnings': True,
            'retries': 10, 'socket_timeout': 60
        }
        if mode == "2":
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            apply_meta = "Y"
            if cfg.GLOBAL_AUTO_METADATA:
                print(f"\n [💎] SGAM ENHANCEMENT:")
            apply_meta = smart_input(" ► Apply SGAM Metadata & Mandatory Tags? (Y/N) [Y]: ").upper() or "Y"
            if apply_meta == '__BACK__': return None
            if apply_meta == "Y":
                print(f" [🏷️] Finalizing Branding & Suffixes...")
                from config import CORE_POSTER_PATH
                if apply_instant_metadata(final_path, CORE_POSTER_PATH):
                    info = get_fast_info(final_path)
                    base, ext = os.path.splitext(final_path)
                    actual_base = os.path.basename(base)
                    new_name = get_smart_filename(actual_base, ext, quality=info['quality'], do_clean=True)
                    new_path = os.path.join(os.path.dirname(final_path), new_name)
                    if final_path != new_path:
                        try:
                            if os.path.exists(new_path): os.remove(new_path)
                            os.rename(final_path, new_path)
                            final_path = new_path
                            smart_name = new_name
                        except: pass
            else:
                base, ext = os.path.splitext(final_path)
                actual_base = os.path.basename(base)
                locked_name = get_smart_filename(actual_base, ext, quality=selected_quality, do_clean=True)
                locked_path = os.path.join(os.path.dirname(final_path), locked_name)
                if final_path != locked_path:
                    try:
                        if os.path.exists(locked_path): os.remove(locked_path)
                        os.rename(final_path, locked_path)
                        smart_name = locked_name
                    except: pass
            success += 1
            queue["pending"].pop(0)
            queue["completed"].append({"url": url, "title": smart_name, "date": time.strftime("%Y-%m-%d")})
            save_queue(queue)
            if cfg.FINISH_SOUND_ALERT:
                try:
                    import winsound
                    winsound.Beep(1000, 400)
                except: pass
            print(f"\n [✓] DONE: {smart_name}")
            if cfg.YOUTUBE_OPEN_FOLDER: os.startfile(out_dir)
            time.sleep(1.5)
        except Exception as e:
            failed += 1
            print(f"\n [✖] FAILED: {e}")
            input("\n Press Enter to continue to next item...")
    t_total = time.time() - t_start
    clear_screen()
    from utils import print_header
    print_header("YOUTUBE PRO", "FINAL REPORT")
    print("  [ FINAL REPORT: YOUTUBE DOWNLOAD ]")
    print("-" * 70)
    print(f"  [+] Success     : {success}")
    print(f"  [-] Failed      : {failed}")
    print(f"  [@] Total Time  : {int(t_total//60)}m {int(t_total%60)}s")
    print("="*70)
    input("\n ► Press Enter to return to Menu...")
if __name__ == "__main__":
    download_youtube_video()