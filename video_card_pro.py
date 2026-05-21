import os
import time
import json
import config as config
from settings_manager import save_preset, load_all_settings, delete_preset
from settings_ui import system_settings_ui
from utils import clear_screen, get_choice, print_header, smart_input
def pick_color(current="white"):
    colors = [
        ("White", "white", "\033[97m"),
        ("Black", "black", "\033[30m"),
        ("Red", "red", "\033[91m"),
        ("Green", "green", "\033[92m"),
        ("Blue", "blue", "\033[94m"),
        ("Yellow", "yellow", "\033[93m"),
        ("Cyan", "cyan", "\033[96m"),
        ("Magenta", "magenta", "\033[95m"),
        ("Gray", "gray", "\033[90m"),
        ("Orange", "orange", "\033[33m"),
        ("Pink", "pink", "\033[95m"),
        ("Purple", "purple", "\033[35m")
    ]
    print("\n Select Color:")
    for i, (name, val, code) in enumerate(colors, 1):
        abbr = (name[:2]).upper()
        print(f"  {i}) {code}{abbr} - {name}\033[0m", end="  ")
        if i % 3 == 0: print()
    print(f"  0) [ BACK ]") 
    choice = input(f"\n Choice (0-12) [{current}]: ").strip()
    if choice == '0' or not choice: return current
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(colors): return colors[idx][1]
    return choice
def layer_editor_ui(l=None):
    if not l:
        l = {
            'type': 'text',
            'timing': {'anchor': 'Start', 'offset': 0, 'duration': 10},
            'content': {'text': ''},
            'style': {'pos': 'Center', 'size_ratio': 15, 'color': 'white', 'opac': 1.0, 'mode': 'Overlay'},
            'animation': {'type': 'None', 'dir': 'In', 'count': 1}
        }
    print(f"\n--- LAYER CONFIGURATION (TEXT ONLY) ---")
    l['type'] = 'text' 
    l['style']['mode'] = 'Overlay'
    l['content']['text'] = input(f" Enter Text [{l['content'].get('text','')}]: ").strip() or l['content'].get('text','')
    print("\n[ RELATIVE TIMING SETUP ]")
    l['timing']['anchor'] = get_choice("Where should this layer appear?", ["Start of Video", "Middle of Video", "End of Video"], default=l['timing'].get('anchor'))
    print(" (Tip: Offset moves the start point; Duration -1 means until the end)")
    l['timing']['offset'] = float(input(f" Time Offset (Seconds) [{l['timing'].get('offset',0)}]: ") or l['timing'].get('offset',0))
    l['timing']['duration'] = float(input(f" Duration (Seconds, use -1 for 'To the end') [{l['timing'].get('duration',10)}]: ") or l['timing'].get('duration',10))
    print("\n[ STYLE & POSITION ]")
    l['style']['pos'] = get_choice("Position:", ["Top-Left", "Top-Center", "Top-Right", "Middle-Left", "Center", "Middle-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right"], default=l['style'].get('pos'))
    l['style']['size_ratio'] = float(input(f" Scale Ratio (Height/X) [{l['style'].get('size_ratio',15)}]: ") or l['style'].get('size_ratio',15))
    l['style']['color'] = pick_color(l['style'].get('color','white'))
    l['style']['opac'] = float(input(f" Opacity (0.1-1.0) [{l['style'].get('opac',1.0)}]: ") or l['style'].get('opac',1.0))
    print("\n[ ANIMATION ]")
    l['animation']['type'] = get_choice("Movement Type:", ["None", "L-R", "R-L", "T-B", "B-T"], default=l['animation'].get('type'))
    if l['animation']['type'] != "None":
        l['animation']['dir'] = get_choice("Movement Direction:", ["In", "Out"], default=l['animation'].get('dir'))
    if l['timing']['anchor'] == "Start of Video":
        l['animation']['count'] = int(input(f" Number of appearances (Looping) [{l['animation'].get('count',1)}]: ") or l['animation'].get('count',1))
    else:
        l['animation']['count'] = 1
    return l
def edit_card_settings(s):
    print("\n[PART 1: VIDEO QUALITY]")
    s['target_q'] = get_choice("Target Resolution:", ["240p", "360p", "480p", "720p", "1080p", "2K", "4K"], default=s.get('target_q', config.DEFAULT_RESOLUTION))
    s['fps'] = input(f"Target FPS [{s.get('fps', str(config.DEFAULT_FPS))}]: ") or s.get('fps', str(config.DEFAULT_FPS))
    br = input(f"Target Bitrate [{s.get('bitrate', config.DEFAULT_BITRATE)}]: ") or s.get('bitrate', config.DEFAULT_BITRATE)
    if br.isdigit(): br += "k"
    s['bitrate'] = br
    print("\n[PART 2: LOGO LAYER]")
    pos_options = ["Top-Left", "Top-Center", "Top-Right", "Middle-Left", "Center", "Middle-Right", "Bottom-Left", "Bottom-Center", "Bottom-Right", "Dynamic-Bounce"]
    s['logo_pos_str'] = get_choice("Logo Position:", pos_options, default=s.get('logo_pos_str','Top-Right'))
    if s['logo_pos_str'] == 'Dynamic-Bounce':
        current_seq = s.get('logo_bounce_seq', 'TL,TR,BR,BL')
        print("  Available: TL (Top-Left), TR (Top-Right), BL (Bottom-Left), BR (Bottom-Right),")
        print("             TC (Top-Center), BC (Bottom-Center), ML (Middle-Left), MR (Middle-Right), C (Center)")
        s['logo_bounce_seq'] = input(f" ► Corners sequence (e.g. TL,TR,BR,BL) [{current_seq}]: ").strip().upper() or current_seq
    s['logo_size'] = float(input(f"Logo Scale % [{s.get('logo_size',20)}]: ") or s.get('logo_size',20))
    s['logo_opac'] = float(input(f"Logo Opacity [{s.get('logo_opac',0.8)}]: ") or s.get('logo_opac',0.8))
    return s
def manage_layers_ui(name, layers):
    while True:
        clear_screen()
        print_header("LAYER MANAGER", f"CARD: {name}")
        if not layers:
            print("\n  [!] No extra layers added yet.")
        else:
            for i, l in enumerate(layers, 1):
                t = l.get('type','text').upper()
                anchor = l.get('timing', {}).get('anchor', 'Start')
                print(f"  {i}) [{t:5}] Pos: {anchor:7} | Mode: {l.get('style',{}).get('mode','Overlay')[:3]}")
        print("\n [A] Add Layer | [E] Edit Layer | [D] Delete Layer | [F] Finish & Save Layers")
        cmd = input("\n Action: ").strip().upper()
        if cmd == 'F': break
        if cmd == 'A': layers.append(layer_editor_ui())
        elif cmd == 'E' and layers:
            try:
                idx = int(input("Layer # to edit: ")) - 1
                layers[idx] = layer_editor_ui(layers[idx])
            except: pass
        elif cmd == 'D' and layers:
            try:
                idx = int(input("Layer # to delete: ")) - 1
                layers.pop(idx); print("\n [OK] Layer Removed."); time.sleep(0.5)
            except: pass
    return layers
def video_card_designer_ui(existing_data=None):
    clear_screen()
    print_header("VIDEO CARD DESIGNER", "PRO EDITOR")
    if not existing_data:
        name = smart_input("\nEnter NEW Video Card Name: ")
        if not name or name == '__BACK__': return
        s = {'card_type': 'Video Card', 'layers': []}
        s = edit_card_settings(s)
        s['layers'] = manage_layers_ui(name, s['layers'])
    else:
        name = existing_data.get('card_name', "Updating...")
        s = existing_data
        while True:
            clear_screen()
            print_header("CARD EDITOR", name.upper())
            print(" 1) Edit Card Settings (Resolution, FPS, Logo)")
            print(" 2) Manage Layers (Add/Edit/Delete Layers)")
            print(" 3) Save & Finish")
            print(" 4) Cancel & Back (Discard Changes)")
            c = input("\n Choice: ").strip()
            if c == '1': s = edit_card_settings(s)
            elif c == '2': s['layers'] = manage_layers_ui(name, s.get('layers', []))
            elif c == '3': 
                save_preset(name, s)
                print(f"\n [SUCCESS] Video Card '{name}' saved.")
                break
            elif c == '4' or c.upper() == 'B': return None
    if name != "Updating...":
        s['card_name'] = name
        save_preset(name, s)
        print(f"\n [SUCCESS] Video Card '{name}' saved."); time.sleep(1)
    return s
def manage_video_cards():
    while True:
        clear_screen()
        presets = load_all_settings()
        video_names = [n for n, d in presets.items() if d.get('card_type', 'Video Card') == "Video Card"]
        print_header("VIDEO CARD MANAGER", "ACTIVE CARDS")
        if not video_names: print("\n [!] No Video Cards Found.")
        else:
            for i, n in enumerate(video_names, 1):
                q = presets[n].get('target_q', '???')
                print(f" {i}) [VIDEO] {n} ({q})")
        print("\n [A] Add Card | [E] Edit | [C] Duplicate | [R] Rename | [D] Delete | [S] System Settings | [B] Back")
        cmd = smart_input("\n Action: ").upper()
        if cmd == 'B' or cmd == '__BACK__' or not cmd: break
        if cmd == 'S': system_settings_ui(); continue
        try:
            if cmd == 'A':
                video_card_designer_ui()
            elif cmd == 'E' and video_names:
                v = smart_input("Card # to edit: ")
                if v == '__BACK__': continue
                idx = int(v) - 1
                video_card_designer_ui(presets[video_names[idx]])
            elif cmd == 'C' and video_names:
                v = smart_input("Card # to duplicate: ")
                if v == '__BACK__': continue
                idx = int(v) - 1
                source = presets[video_names[idx]].copy()
                new_n = smart_input(f"New Name: ")
                if new_n == '__BACK__': continue
                if new_n:
                    source['card_name'] = new_n
                    save_preset(new_n, source)
            elif cmd == 'R' and video_names:
                v = smart_input("Card # to rename: ")
                if v == '__BACK__': continue
                idx = int(v) - 1
                new_n = smart_input("New Name: ")
                if new_n == '__BACK__': continue
                if new_n:
                    data = presets[video_names[idx]]
                    data['card_name'] = new_n
                    delete_preset(video_names[idx])
                    save_preset(new_n, data)
            elif cmd == 'D' and video_names:
                v = smart_input("Card # to delete: ")
                if v == '__BACK__': continue
                idx = int(v) - 1
                delete_preset(video_names[idx])
        except Exception as e: print(f"Error: {e}"); time.sleep(1)
if __name__ == "__main__":
    manage_video_cards()