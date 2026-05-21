import os
import shutil
import time

# إعدادات المسارات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_PKG = os.path.join(BASE_DIR, "sgam_processor")
SOURCE_LAUNCHER = os.path.join(BASE_DIR, "launcher.py")
BACKUP_DIR = os.path.join(BASE_DIR, "SGAM_SAFE_BACKUP")

from utils import clear, print_header

def perform_backup():
    print("\n [>] Starting Backup Process...")
    
    # 1. حذف النسخة القديمة إذا وجدت لضمان التحديث
    if os.path.exists(BACKUP_DIR):
        print(" [!] Removing old backup...")
        shutil.rmtree(BACKUP_DIR)
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # 2. نسخ مجلد المشروع بالكامل
    try:
        print(" [!] Copying 'sgam_processor'...")
        shutil.copytree(SOURCE_PKG, os.path.join(BACKUP_DIR, "sgam_processor"))
        
        print(" [!] Copying 'launcher.py'...")
        shutil.copy2(SOURCE_LAUNCHER, os.path.join(BACKUP_DIR, "launcher.py"))
        
        print("\n [SUCCESS] Backup created successfully in 'SGAM_SAFE_BACKUP'.")
    except Exception as e:
        print(f"\n [ERROR] Backup failed: {e}")

def perform_restore():
    if not os.path.exists(BACKUP_DIR):
        print("\n [!] No backup folder found! Cannot restore.")
        return

    print("\n [!!!] WARNING: This will overwrite your CURRENT files with the backup.")
    confirm = input(" [?] Are you sure you want to restore? (YES/NO): ").strip().upper()
    
    if confirm == 'YES':
        try:
            print(" [!] Removing current files...")
            if os.path.exists(SOURCE_PKG): shutil.rmtree(SOURCE_PKG)
            
            print(" [!] Restoring files from backup...")
            shutil.copytree(os.path.join(BACKUP_DIR, "sgam_processor"), SOURCE_PKG)
            shutil.copy2(os.path.join(BACKUP_DIR, "launcher.py"), SOURCE_LAUNCHER)
            
            print("\n [SUCCESS] System restored to previous state successfully!")
        except Exception as e:
            print(f"\n [ERROR] Restore failed: {e}")
    else:
        print("\n [X] Restore cancelled.")

def main():
    while True:
        print_header()
        print(" [1] 📤 CREATE NEW BACKUP (Overwrite previous)")
        print(" [2] 📥 RESTORE SYSTEM    (Back to previous state)")
        print("-" * 55)
        print(" [Q] EXIT")
        print("-" * 55)
        
        choice = input(" ► Selection: ").strip().upper()
        
        if choice == '1':
            perform_backup()
            input("\nPress Enter to return...")
        elif choice == '2':
            perform_restore()
            input("\nPress Enter to return...")
        elif choice == 'Q':
            break

if __name__ == "__main__":
    main()
