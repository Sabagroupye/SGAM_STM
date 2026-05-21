import os
import config as config

from utils import timestamp_to_seconds, smart_input

def get_batch_censor_config():
    print("\n [!] Batch Mode: Same timing will apply to all files.")
    print("  Available Formats:")
    print("  • 10-20         (Seconds 10 to 20)")
    print("  • 01:30-02:00   (Minutes 1:30 to 2:00)")
    print("  • 10-20, 40-50  (Multiple segments with comma)")
    ts_in = smart_input("\n ► Enter Timing (e.g. 10-15, 1:00-1:05): ")
    if ts_in == '__BACK__': return None
    if ts_in:
        ivs = []
        for part in ts_in.split(','):
            try: 
                b = part.split('-')
                ivs.append((timestamp_to_seconds(b[0]), timestamp_to_seconds(b[1]) if len(b)>1 else timestamp_to_seconds(b[0])+5))
            except: pass
        if ivs:
            print("\n ► Select Block Type: [1] Freeze | [2] Cut | [3] Blur | [B] Back")
            cm = smart_input(" ► Selection [1]: ").upper() or "1"
            if cm == '__BACK__': return None
            c_mode = {"1":"Freeze","2":"Cut","3":"Blur"}.get(cm,"Freeze")
            c_data = {"ivs": ivs, "mode": c_mode}
            
            if c_mode == "Cut":
                print("\n  ➔ [1] Standard Cut (Remove Periods)")
                print("  ➔ [2] Keep Mode     (Time Periods Only - FAST)")
                cut_m = smart_input(" ► Selection [1]: ") or "1"
                if cut_m == '__BACK__': return None
                if cut_m == "2": c_data["keep_only"] = True
            
            return c_data
    return None

def get_individual_censor_config(video_path, dur):
    from utils import print_header
    print_header("VIDEO HUB", "CENSOR SETUP")

    if config.AUTO_PREVIEW_ORIGINAL:
        print(f"\n [🎬] Launching Preview: {os.path.basename(video_path)}")
        try: 
            os.startfile(video_path)
            import time
            time.sleep(1)
        except: pass
    
    print(f"  • Duration: {int(dur)}s")
    print("  [!] Seconds: 10-20 | Minutes: 1:30-2:00 | Hours: 01:05:00-01:06:00")
    ts_in = smart_input(f" ► Censor Timing: ")
    if ts_in == '__BACK__': return "BACK"
    
    if ts_in:
        ivs = []; parts = ts_in.split(',')
        for p in parts:
            try: 
                b = p.split('-')
                start_s = timestamp_to_seconds(b[0], dur)
                end_s = timestamp_to_seconds(b[1], dur) if len(b)>1 else start_s + 5
                ivs.append((start_s, end_s))
            except: pass
        if ivs:
            print("  ➔ [1] Freeze | [2] Cut | [3] Blur | [B] Back")
            cm = smart_input(" ► Selection [1]: ").upper() or "1"
            if cm == 'B' or cm == '__BACK__': return "BACK"
            c_mode = {"1":"Freeze","2":"Cut","3":"Blur"}.get(cm,"Freeze")
            c_data = {"ivs": ivs, "mode": c_mode}
            
            if c_mode == "Cut":
                print("\n  ➔ [1] Standard Cut (Remove Periods)")
                print("  ➔ [2] Keep Mode     (Time Periods Only - FAST)")
                cut_m = smart_input(" ► Selection [1]: ") or "1"
                if cut_m == '__BACK__': return "BACK"
                if cut_m == "2": c_data["keep_only"] = True
                
                ans_save = smart_input(" ► Save CUT segments as clips? [Y/N]: ").upper()
                if ans_save == '__BACK__': return "BACK"
                if ans_save == 'Y': c_data["save_cuts"] = True
            return c_data
    return None
