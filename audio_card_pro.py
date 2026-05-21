import os
import time
import config as config
from settings_manager import save_preset, load_all_settings, delete_preset
from utils import clear_screen, get_choice, print_header, smart_input
def audio_card_designer_ui(existing_data=None):
    clear_screen()
    print_header("AUDIO CARD DESIGNER", "PRO EDITOR")
    if not existing_data:
        name = smart_input("\nEnter NEW Audio Card Name: ")
        if not name or name == '__BACK__': return
    else:
        name = existing_data.get('card_name', "Updating...")
    s = existing_data or {'card_type': 'Audio Card'}
    print("\n[PART 1: AUDIO SPECS]")
    s['target_format'] = get_choice("Target Format:", ["MP3", "WAV", "AAC"], default=s.get('target_format', "MP3"))
    br = input(f"Target Bitrate (e.g. 128k, 192k, 320k) [{s.get('bitrate', config.AUDIO_QUALITY)}]: ") or s.get('bitrate', config.AUDIO_QUALITY)
    if br.isdigit(): br += "k"
    s['bitrate'] = br
    print("\n[PART 2: BRANDING & MIXING]")
    s['watermark_mix'] = get_choice("Enable Audio Watermark Mixing?", ["Yes", "No"], default=s.get('watermark_mix', "Yes"))
    if s['watermark_mix'] == "Yes":
        s['sig_location'] = get_choice("Signature Location:", ["Start", "End"], default=s.get('sig_location', config.AUDIO_SIGNATURE_LOCATION))
        off = input(f"Offset in Seconds [{s.get('sig_offset', config.AUDIO_SIGNATURE_OFFSET)}]: ") or s.get('sig_offset', config.AUDIO_SIGNATURE_OFFSET)
        try: s['sig_offset'] = float(off)
        except: s['sig_offset'] = config.AUDIO_SIGNATURE_OFFSET
    print("\n[PART 3: STORAGE]")
    s['out_mode_str'] = get_choice("Output Storage Mode:", ["Mirror (Keep Folders)", "Flat (One Output Folder)"], default=s.get('out_mode_str', "1"))
    if name != "Updating...":
        s['card_name'] = name
        save_preset(name, s)
        print(f"\n [SUCCESS] Audio Card '{name}' saved with full specs.")
        time.sleep(0.5)
    return s
def manage_audio_cards():
    while True:
        clear_screen()
        presets = load_all_settings()
        audio_names = [n for n, d in presets.items() if d.get('card_type') == "Audio Card"]
        print_header("AUDIO CARD MANAGER", "ACTIVE CARDS")
        if not audio_names: print("\n [!] No Audio Cards Found.")
        else:
            for i, n in enumerate(audio_names, 1):
                fmt = presets[n].get('target_format', 'MP3')
                br = presets[n].get('bitrate', '???')
                print(f" {i}) [AUDIO] {n} ({fmt} @ {br})")
        print("\n [A] Add Card | [E] Edit | [C] Duplicate | [R] Rename | [D] Delete | [B] Back")
        cmd = smart_input("\n Action: ").upper()
        if cmd == 'B' or cmd == '__BACK__' or not cmd: break
        try:
            if cmd == 'A': audio_card_designer_ui()
            elif cmd == 'E' and audio_names:
                v = smart_input("Card # to edit: ")
                if v == '__BACK__': continue
                idx = int(v) - 1
                updated = audio_card_designer_ui(presets[audio_names[idx]])
                if updated: save_preset(audio_names[idx], updated)
            elif cmd == 'C' and audio_names:
                v = smart_input("Card # to duplicate: ")
                if v == '__BACK__': continue
                idx = int(v) - 1
                source = presets[audio_names[idx]].copy()
                new_n = smart_input(f"New Name for Duplicate of '{audio_names[idx]}': ")
                if new_n == '__BACK__': continue
                if new_n:
                    source['card_name'] = new_n
                    save_preset(new_n, source)
            elif cmd == 'R' and audio_names:
                v = smart_input("Card # to rename: ")
                if v == '__BACK__': continue
                idx = int(v) - 1
                new_n = smart_input("New Name: ")
                if new_n == '__BACK__': continue
                if new_n:
                    data = presets[audio_names[idx]]
                    data['card_name'] = new_n
                    delete_preset(audio_names[idx])
                    save_preset(new_n, data)
            elif cmd == 'D' and audio_names:
                v = smart_input("Card # to delete: ")
                if v == '__BACK__': continue
                idx = int(v) - 1
                delete_preset(audio_names[idx])
        except Exception as e: print(f"Error: {e}"); time.sleep(0.5)
if __name__ == "__main__":
    manage_audio_cards()