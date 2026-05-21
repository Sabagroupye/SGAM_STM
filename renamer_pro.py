import os
import time
from utils import clear_screen, smart_input
def smart_renamer_ui(paths):
    from utils import print_header
    clear_screen()
    print_header("SMART RENAMER", f"{len(paths)} ITEMS READY")
    print(f"\n [!] Target Items: {len(paths)}")
    print("\n [ SELECT ACTION ]")
    print("  1) Find & Replace Text")
    print("  2) Add Prefix (Start of Name)")
    print("  3) Add Suffix (End of Name)")
    print("  B) Back")
    choice = smart_input("\n ► Selection: ").upper()
    if choice == '__BACK__' or choice == 'B': return
    old_txt = ""
    new_txt = ""
    if choice == '1':
        old_txt = smart_input("\n ► Text to FIND: ")
        if old_txt == '__BACK__': return
        new_txt = smart_input(" ► Text to REPLACE with: ")
        if new_txt == '__BACK__': return
    elif choice == '2':
        new_txt = smart_input("\n ► Text to ADD at START: ")
        if new_txt == '__BACK__': return
    elif choice == '3':
        new_txt = smart_input("\n ► Text to ADD at END: ")
        if new_txt == '__BACK__': return
    else: return
    print("\n [ SELECT SCOPE ]")
    print("  1) Files Only")
    print("  2) Folders Only")
    print("  3) Both (Everything)")
    scope = smart_input("\n ► Target Scope [3]: ") or '3'
    if scope == '__BACK__': return
    is_recursive = 'N'
    if any(os.path.isdir(p) for p in paths):
        is_recursive = smart_input("\n ► Include subfolders? (Y/N) [Y]: ").upper() or 'Y'
        if is_recursive == '__BACK__': return
    print("\n [⏳] Renaming in progress...")
    print("-" * 50)
    s_count, e_count = 0, 0
    def process_item(item_path):
        nonlocal s_count, e_count
        try:
            is_dir = os.path.isdir(item_path)
            if scope == '1' and is_dir: return
            if scope == '2' and not is_dir: return
            parent = os.path.dirname(item_path)
            old_name = os.path.basename(item_path)
            from tag_logic import get_system_tag
            mandatory = get_system_tag() 
            placeholder = "___SGAM_PROTECTED___"
            protected_name = old_name.replace(mandatory, placeholder)
            new_name = protected_name
            if choice == '1': 
                if old_txt in protected_name:
                    new_name = protected_name.replace(old_txt, new_txt)
            elif choice == '2': 
                if not protected_name.startswith(new_txt):
                    new_name = new_txt + protected_name
            elif choice == '3': 
                base, ext = os.path.splitext(protected_name)
                if not base.endswith(new_txt):
                    new_name = base + new_txt + ext
            if placeholder in new_name:
                final_temp_name = new_name.replace(placeholder, mandatory)
            else:
                base, ext = os.path.splitext(new_name)
                from utils import get_smart_filename
                final_temp_name = get_smart_filename(base, ext, is_folder=is_dir)
            base_final, ext_final = os.path.splitext(final_temp_name)
            from utils import get_smart_filename
            final_output_name = get_smart_filename(base_final, ext_final, is_folder=is_dir, do_clean=True)
            if old_name != final_output_name:
                new_path = os.path.join(parent, final_output_name)
                from utils import ensure_unique_path
                new_path = ensure_unique_path(new_path, source_path=item_path)
                if not os.path.exists(new_path):
                    os.rename(item_path, new_path)
                    s_count += 1
                else:
                    print(f" [!] Skip: Name conflict: {os.path.basename(new_path)}")
        except Exception as e:
            e_count += 1
            print(f" [✖] Error renaming {os.path.basename(item_path)}: {e}")
    for p in paths:
        if os.path.isdir(p) and is_recursive == 'Y':
            for root, dirs, files in os.walk(p, topdown=False):
                for name in files:
                    process_item(os.path.join(root, name))
                for name in dirs:
                    process_item(os.path.join(root, name))
            process_item(p)
        else:
            process_item(p)
    print("\n" + "="*40)
    print("         FINAL RENAME REPORT          ")
    print("="*40)
    print(f"  [+] Success Transformations : {s_count}")
    print(f"  [-] Errors / Skipped        : {e_count}")
    print("="*40)
    smart_input("\n ► Press Enter to continue...")