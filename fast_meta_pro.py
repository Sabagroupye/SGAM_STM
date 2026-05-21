import os
import sys
import time
from utils import clear_screen, get_smart_filename, ensure_unique_path, smart_input
from metadata import apply_instant_metadata, get_fast_info
from internal_paths import CORE_POSTER

def quick_sweep(media_list, root_dir):
    from utils import print_header, launch_cpu_monitor
    launch_cpu_monitor()
    print_header("INSTANT METADATA SWEEP")
    print(f"\n [🏷️] Selected Files: {len(media_list)}")
    print(" [!] Logic: Instant Mutagen Injection + Smart Auto-Rename")
    print(" [!] Note : Files will be updated and renamed in-place.")
    print("-" * 70)
    
    ans = smart_input("\n ► Clean names? (Y/N) [Y]: ").upper() or 'Y'
    if ans == '__BACK__': return
    do_clean = (ans == 'Y')
    
    success, failed = 0, 0
    t_start = time.time()
    
    for i, f in enumerate(media_list, 1):
        try:
            if not os.path.exists(f): continue
            
            old_fname = os.path.basename(f)
            print(f" [{i}/{len(media_list)}] [WORK] Processing: {old_fname[:50]}".ljust(100), end="\r")
            
            if apply_instant_metadata(f, CORE_POSTER):
                info = get_fast_info(f)
                quality = info["quality"]
                
                base_part, ext_part = os.path.splitext(old_fname)
                new_fname = get_smart_filename(base_part, ext_part, quality=quality, do_clean=do_clean)
                
                new_path = os.path.join(os.path.dirname(f), new_fname)
                
                if f != new_path:
                    new_path = ensure_unique_path(new_path, source_path=f)
                    os.rename(f, new_path)
                
                success += 1
            else:
                failed += 1
                print(f"\n [!] Metadata Injection Failed: {old_fname}")
                
        except Exception as e:
            print(f"\n [!] Error at {os.path.basename(f)}: {e}")
            failed += 1

    t_total = time.time() - t_start
    print(f"\n\n{'='*60}")
    print("      FINAL METADATA & RENAME REPORT      ")
    from config import FINISH_SOUND_ALERT
    if FINISH_SOUND_ALERT:
        try:
            import winsound
            winsound.Beep(1000, 600)
        except: pass
    print(f"{'='*60}")
    print(f" [✔] SUCCESSFUL : {success}")
    print(f" [✖] FAILED     : {failed}")
    print(f" [@] TOTAL TIME : {t_total:.2f}s")
    print("-" * 60)
    
    smart_input("\n ► Press [ENTER] to return to hub...")
