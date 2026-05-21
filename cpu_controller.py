import os
import sys
import time
try:
    import psutil
except ImportError:
    print("This controller requires 'psutil' library.")
    print("Please install it by running: pip install psutil")
    input("\nPress Enter to exit...")
    sys.exit()
from utils import clear, smart_input

def get_ffmpeg_procs():
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'status']):
        try:
            if 'ffmpeg' in p.info['name'].lower():
                procs.append(p)
        except: pass
    return procs

def main():
    status_msg = ""
    # Query cpu_percent once initially to register the first state
    for p in get_ffmpeg_procs():
        try: p.cpu_percent(interval=None)
        except: pass
        
    while True:
        clear()
        print("=======================================================")
        print("      SABA GROUP - CPU & PROCESS CONTROLLER            ")
        print("=======================================================")
        
        if status_msg:
            print(f"\n [📢] STATUS: {status_msg}")
            print("=" * 55)
            status_msg = ""
            
        procs = get_ffmpeg_procs()
        if not procs:
            print("\n [INFO] No running FFmpeg processes found.")
        else:
            print(f"\n Found {len(procs)} active processes:\n")
            for i, p in enumerate(procs, 1):
                try:
                    cpu = p.cpu_percent(interval=None)
                    print(f"  {i}) PID: {p.pid} | Status: {p.status()} | CPU: {cpu:.1f}%")
                except Exception as e:
                    print(f"  {i}) PID: {p.pid} | Error: {e}")
                    
        print("\n" + "-"*40)
        print(" 1) Refresh List                  (تحديث القائمة)")
        if procs:
            print(" 2) SUSPEND (Pause) All Processes  (إيقاف مؤقت للكل)")
            print(" 3) RESUME (Start) All Processes   (استئناف الكل)")
            print(" 4) SET PRIORITY TO IDLE           (أولوية منخفضة جداً)")
            print(" 5) SET PRIORITY TO NORMAL         (أولوية طبيعية)")
            print(" 6) KILL All Processes             (إنهاء كافة العمليات)")
        print(" Q) Quit Controller                (خروج)")
        print("-" * 40)
        
        choice = smart_input(" Select Action: ").upper()
        if choice in ('Q', 'B', '__BACK__'):
            break
        elif choice == '1':
            continue
        elif not procs:
            status_msg = "No processes to act on."
            continue
            
        actions_taken = []
        for p in procs:
            try:
                if choice == '2':
                    p.suspend()
                    actions_taken.append(f"Suspended {p.pid}")
                elif choice == '3':
                    p.resume()
                    actions_taken.append(f"Resumed {p.pid}")
                elif choice == '4':
                    p.nice(psutil.IDLE_PRIORITY_CLASS)
                    actions_taken.append(f"PID {p.pid} -> IDLE")
                elif choice == '5':
                    p.nice(psutil.NORMAL_PRIORITY_CLASS)
                    actions_taken.append(f"PID {p.pid} -> NORMAL")
                elif choice == '6':
                    p.terminate()
                    actions_taken.append(f"Terminated {p.pid}")
            except Exception as e:
                actions_taken.append(f"PID {p.pid} Error: {str(e)}")
                
        if actions_taken:
            status_msg = " | ".join(actions_taken)
            time.sleep(0.5)

if __name__ == "__main__":
    main()