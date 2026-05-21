import os
import time
import config as config
from utils import clear_screen, get_choice, smart_input
def import_metadata_from_file():
    path = config.METADATA_TEXT_PATH
    if not os.path.exists(path):
        print(f"\n [!] Error: File not found at {path}")
        time.sleep(1.5)
        return False
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        mapping = {
            "العنوان": "TITLE",
            "الفنان": "ARTIST",
            "الألبوم": "ALBUM_NAME",
            "السنة": "DATE_YEAR",
            "رقم المقطع": "TRACK_NUMBER",
            "النوع": "GENRE",
            "التعليق": "COMMENT",
            "فنان الألبوم": "ALBUM_ARTIST",
            "الملحن": "COMPOSER"
        }
        found_any = False
        for line in lines:
            if ':' in line:
                key_ar, val = line.split(':', 1)
                key_ar = key_ar.strip()
                val = val.strip()
                if key_ar in mapping:
                    setattr(config, mapping[key_ar], val)
                    found_any = True
        if found_any:
            save_all_to_config()
            print("\n [SUCCESS] Metadata imported from text file!")
            time.sleep(1.2)
            return True
        else:
            print("\n [!] No valid metadata fields found in file.")
            time.sleep(1.5)
            return False
    except Exception as e:
        print(f"\n [!] Import Error: {e}")
        time.sleep(1.5)
        return False
def save_all_to_config():
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.py')
    if not os.path.exists(conf_path): return
    with open(conf_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(conf_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.startswith('COMPANY_URL ='): f.write(f'COMPANY_URL = "{config.COMPANY_URL}"\n')
            elif line.startswith('BRANDING_TEXT ='): f.write(f'BRANDING_TEXT = "{config.BRANDING_TEXT}"\n')
            elif line.startswith('CORE_LOGO_PATH ='): f.write(f'CORE_LOGO_PATH = r"{config.CORE_LOGO_PATH}"\n')
            elif line.startswith('FILE_SUFFIX ='): f.write(f'FILE_SUFFIX = "{config.FILE_SUFFIX}"\n')
            elif line.startswith('TITLE ='): f.write(f'TITLE = "{config.TITLE}"\n')
            elif line.startswith('ARTIST ='): f.write(f'ARTIST = "{config.ARTIST}"\n')
            elif line.startswith('ALBUM_NAME ='): f.write(f'ALBUM_NAME = "{config.ALBUM_NAME}"\n')
            elif line.startswith('ALBUM_ARTIST ='): f.write(f'ALBUM_ARTIST = "{config.ALBUM_ARTIST}"\n')
            elif line.startswith('GENRE ='): f.write(f'GENRE = "{config.GENRE}"\n')
            elif line.startswith('COMPOSER ='): f.write(f'COMPOSER = "{config.COMPOSER}"\n')
            elif line.startswith('COMMENT ='): f.write(f'COMMENT = "{config.COMMENT}"\n')
            elif line.startswith('DATE_YEAR ='): f.write(f'DATE_YEAR = "{config.DATE_YEAR}"\n')
            elif line.startswith('TRACK_NUMBER ='): f.write(f'TRACK_NUMBER = "{config.TRACK_NUMBER}"\n')
            elif line.startswith('GLOBAL_AUTO_METADATA ='): f.write(f'GLOBAL_AUTO_METADATA = {config.GLOBAL_AUTO_METADATA}\n')
            elif line.startswith('DEFAULT_RESOLUTION ='): f.write(f'DEFAULT_RESOLUTION = "{config.DEFAULT_RESOLUTION}"\n')
            elif line.startswith('DEFAULT_BITRATE ='): f.write(f'DEFAULT_BITRATE = "{config.DEFAULT_BITRATE}"\n')
            elif line.startswith('DEFAULT_FPS ='): f.write(f'DEFAULT_FPS = {config.DEFAULT_FPS}\n')
            elif line.startswith('BLUR_INTENSITY ='): f.write(f'BLUR_INTENSITY = "{config.BLUR_INTENSITY}"\n')
            elif line.startswith('DEFAULT_TEXT_COLOR ='): f.write(f'DEFAULT_TEXT_COLOR = "{config.DEFAULT_TEXT_COLOR}"\n')
            elif line.startswith('DEFAULT_TEXT_RATIO ='): f.write(f'DEFAULT_TEXT_RATIO = {config.DEFAULT_TEXT_RATIO}\n')
            elif line.startswith('IGNORE_LOWER_QUALITY ='): f.write(f'IGNORE_LOWER_QUALITY = {config.IGNORE_LOWER_QUALITY}\n')
            elif line.startswith('IGNORE_EQUAL_QUALITY ='): f.write(f'IGNORE_EQUAL_QUALITY = {config.IGNORE_EQUAL_QUALITY}\n')
            elif line.startswith('SAVE_CENSOR_CUTS ='): f.write(f'SAVE_CENSOR_CUTS = {config.SAVE_CENSOR_CUTS}\n')
            elif line.startswith('OVERWRITE_ORIGINAL ='): f.write(f'OVERWRITE_ORIGINAL = {config.OVERWRITE_ORIGINAL}\n')
            elif line.startswith('AUDIO_QUALITY ='): f.write(f'AUDIO_QUALITY = "{config.AUDIO_QUALITY}"\n')
            elif line.startswith('DEFAULT_AUDIO_FORMAT ='): f.write(f'DEFAULT_AUDIO_FORMAT = "{config.DEFAULT_AUDIO_FORMAT}"\n')
            elif line.startswith('AUDIO_SIGNATURE_AUTO ='): f.write(f'AUDIO_SIGNATURE_AUTO = "{config.AUDIO_SIGNATURE_AUTO}"\n')
            elif line.startswith('AUDIO_SIGNATURE_PATH ='): f.write(f'AUDIO_SIGNATURE_PATH = r"{config.AUDIO_SIGNATURE_PATH}"\n')
            elif line.startswith('AUDIO_SIGNATURE_SIG_VOL ='): f.write(f'AUDIO_SIGNATURE_SIG_VOL = {config.AUDIO_SIGNATURE_SIG_VOL}\n')
            elif line.startswith('AUDIO_SIGNATURE_MAIN_VOL ='): f.write(f'AUDIO_SIGNATURE_MAIN_VOL = {config.AUDIO_SIGNATURE_MAIN_VOL}\n')
            elif line.startswith('AUDIO_SIGNATURE_MODE ='): f.write(f'AUDIO_SIGNATURE_MODE = "{config.AUDIO_SIGNATURE_MODE}"\n')
            elif line.startswith('AUDIO_SIGNATURE_OFFSET ='): f.write(f'AUDIO_SIGNATURE_OFFSET = {config.AUDIO_SIGNATURE_OFFSET}\n')
            elif line.startswith('LOGO_BOUNCE_WAIT ='): f.write(f'LOGO_BOUNCE_WAIT = "{config.LOGO_BOUNCE_WAIT}"\n')
            elif line.startswith('LOGO_BOUNCE_LINKED_TO_DURATION ='): f.write(f'LOGO_BOUNCE_LINKED_TO_DURATION = {config.LOGO_BOUNCE_LINKED_TO_DURATION}\n')
            elif line.startswith('MAIN_SEPARATOR ='): f.write(f'MAIN_SEPARATOR = "{config.MAIN_SEPARATOR}"\n')
            elif line.startswith('NAME_SEPARATOR ='): f.write(f'NAME_SEPARATOR = "{config.NAME_SEPARATOR}"\n')
            elif line.startswith('RENAME_ORIGINAL_ON_ALL ='): f.write(f'RENAME_ORIGINAL_ON_ALL = {config.RENAME_ORIGINAL_ON_ALL}\n')
            elif line.startswith('AUTO_PREVIEW_ORIGINAL ='): f.write(f'AUTO_PREVIEW_ORIGINAL = {config.AUTO_PREVIEW_ORIGINAL}\n')
            elif line.startswith('REMOVE_WORDS ='): f.write(f'REMOVE_WORDS = {config.REMOVE_WORDS}\n')
            elif line.startswith('REMOVE_SYMBOLS ='): f.write(f'REMOVE_SYMBOLS = {config.REMOVE_SYMBOLS}\n')
            elif line.startswith('BASE_TEXT_ENABLED ='): f.write(f'BASE_TEXT_ENABLED = {config.BASE_TEXT_ENABLED}\n')
            elif line.startswith('BASE_TEXT_DURATION ='): f.write(f'BASE_TEXT_DURATION = {config.BASE_TEXT_DURATION}\n')
            elif line.startswith('BASE_TEXT_POS ='): f.write(f'BASE_TEXT_POS = "{config.BASE_TEXT_POS}"\n')
            elif line.startswith('BASE_TEXT_COLOR ='): f.write(f'BASE_TEXT_COLOR = "{config.BASE_TEXT_COLOR}"\n')
            elif line.startswith('BASE_TEXT_OPACITY ='): f.write(f'BASE_TEXT_OPACITY = {config.BASE_TEXT_OPACITY}\n')
            elif line.startswith('BASE_TEXT_START ='): f.write(f'BASE_TEXT_START = {config.BASE_TEXT_START}\n')
            elif line.startswith('BASE_TEXT_SIZE_RATIO ='): f.write(f'BASE_TEXT_SIZE_RATIO = {config.BASE_TEXT_SIZE_RATIO}\n')
            elif line.startswith('BASE_TEXT_MOVE_TYPE ='): f.write(f'BASE_TEXT_MOVE_TYPE = "{config.BASE_TEXT_MOVE_TYPE}"\n')
            elif line.startswith('BASE_TEXT_APPEAR_COUNT ='): f.write(f'BASE_TEXT_APPEAR_COUNT = {config.BASE_TEXT_APPEAR_COUNT}\n')
            elif line.startswith('VIDEO_OUTPUT_PATH ='): f.write(f'VIDEO_OUTPUT_PATH = r"{config.VIDEO_OUTPUT_PATH}"\n')
            elif line.startswith('AUDIO_OUTPUT_PATH ='): f.write(f'AUDIO_OUTPUT_PATH = r"{config.AUDIO_OUTPUT_PATH}"\n')
            elif line.startswith('GLOBAL_CLIPS_OUTPUT_PATH ='): f.write(f'GLOBAL_CLIPS_OUTPUT_PATH = r"{config.GLOBAL_CLIPS_OUTPUT_PATH}"\n')
            elif line.startswith('YOUTUBE_DOWNLOAD_PATH ='): f.write(f'YOUTUBE_DOWNLOAD_PATH = r"{config.YOUTUBE_DOWNLOAD_PATH}"\n')
            elif line.startswith('YOUTUBE_OPEN_FOLDER ='): f.write(f'YOUTUBE_OPEN_FOLDER = {config.YOUTUBE_OPEN_FOLDER}\n')
            elif line.startswith('YOUTUBE_FINISHED_SOUND ='): f.write(f'YOUTUBE_FINISHED_SOUND = {config.YOUTUBE_FINISHED_SOUND}\n')
            elif line.startswith('YOUTUBE_SMART_NAMING ='): f.write(f'YOUTUBE_SMART_NAMING = {config.YOUTUBE_SMART_NAMING}\n')
            elif line.startswith('CPU_PRIORITY ='): f.write(f'CPU_PRIORITY = "{config.CPU_PRIORITY}"\n')
            elif line.startswith('FINISH_SOUND_ALERT ='): f.write(f'FINISH_SOUND_ALERT = {config.FINISH_SOUND_ALERT}\n')
            elif line.startswith('AUTO_OPEN_CPU_MONITOR ='): f.write(f'AUTO_OPEN_CPU_MONITOR = {getattr(config, "AUTO_OPEN_CPU_MONITOR", False)}\n')
            elif line.startswith('DEFAULT_FONT_PATH ='): f.write(f'DEFAULT_FONT_PATH = r"{config.DEFAULT_FONT_PATH}"\n')
            elif line.startswith('CORE_ASSETS_DIR ='): f.write(f'CORE_ASSETS_DIR = r"{config.CORE_ASSETS_DIR}"\n')
            elif line.startswith('CORE_POSTER_PATH ='): f.write(f'CORE_POSTER_PATH = r"{config.CORE_POSTER_PATH}"\n')
            elif line.startswith('METADATA_TEXT_PATH ='): f.write(f'METADATA_TEXT_PATH = r"{config.METADATA_TEXT_PATH}"\n')
            elif line.startswith('INCLUDE_USER_SUFFIX ='): f.write(f'INCLUDE_USER_SUFFIX = {config.INCLUDE_USER_SUFFIX}\n')
            elif line.startswith('INCLUDE_QUALITY_IN_NAME ='): f.write(f'INCLUDE_QUALITY_IN_NAME = {config.INCLUDE_QUALITY_IN_NAME}\n')
            elif line.startswith('DEFAULT_CLIP_MODE ='): f.write(f'DEFAULT_CLIP_MODE = "{config.DEFAULT_CLIP_MODE}"\n')
            elif line.startswith('DEFAULT_CLIP_DURATION ='): f.write(f'DEFAULT_CLIP_DURATION = {config.DEFAULT_CLIP_DURATION}\n')
            elif line.startswith('DEFAULT_CLIPS_DIR_NAME ='): f.write(f'DEFAULT_CLIPS_DIR_NAME = "{config.DEFAULT_CLIPS_DIR_NAME}"\n')
            else: f.write(line)

def system_settings_ui():
    while True:
        from utils import print_header
        print_header("SYSTEM CONFIG", "GLOBAL SETTINGS")
        print("\n [ 1: IDENTITY & BRANDING ]")
        print(f"  1) Company URL     : {config.COMPANY_URL}")
        print(f"  2) Branding Text   : {config.BRANDING_TEXT}")
        print(f"  3) Core Logo Path  : {config.CORE_LOGO_PATH}")
        print(f"  4) Filename Suffix : {config.FILE_SUFFIX}")
        print("\n [ 2: METADATA ENGINE ]")
        print(f"  5) Global Title    : {config.TITLE if config.TITLE else '[Branding]'}")
        print(f"  6) Global Artist   : {config.ARTIST}")
        print(f"  7) Album Name      : {config.ALBUM_NAME}")
        print(f"  8) Year            : {config.DATE_YEAR}")
        print(f"  9) Track Number    : {config.TRACK_NUMBER}")
        print(f"  10) Genre          : {config.GENRE}")
        print(f"  11) Composer       : {config.COMPOSER}")
        print(f"  12) Album Artist   : {config.ALBUM_ARTIST}")
        print(f"  13) Comment        : {config.COMMENT}")
        print(f"  14) Meta.txt Path  : {config.METADATA_TEXT_PATH}")
        print(f"  15) AutoMeta       : {'[ON]' if config.GLOBAL_AUTO_METADATA else '[OFF]'}")
        print(f"  [S] SYNC FROM metadata.txt")
        print("\n [ 3: VIDEO ENGINE ]")
        print(f"  16) Resolution     : {config.DEFAULT_RESOLUTION}")
        print(f"  17) Bitrate        : {config.DEFAULT_BITRATE}")
        print(f"  18) FPS            : {config.DEFAULT_FPS}")
        print(f"  19) Blur Intensity : {config.BLUR_INTENSITY}")
        print(f"  20) Text Color     : {config.DEFAULT_TEXT_COLOR}")
        print(f"  21) Text Size Ratio: {config.DEFAULT_TEXT_RATIO}")
        print(f"  22) Ignore Lower Q : {'[YES]' if config.IGNORE_LOWER_QUALITY else '[NO]'}")
        print(f"  23) Ignore Equal Q : {'[YES]' if config.IGNORE_EQUAL_QUALITY else '[NO]'}")
        print(f"  24) Save Cuts      : {'[ENABLED]' if config.SAVE_CENSOR_CUTS else '[DISABLED]'}")
        print(f"  25) Overwrite Orig : {'[YES]' if config.OVERWRITE_ORIGINAL else '[NO]'}")
        print(f"  26) Rename Orig.   : {'[YES]' if config.RENAME_ORIGINAL_ON_ALL else '[NO]'}")
        print("\n [ 4: AUDIO ENGINE ]")
        print(f"  27) Audio Quality  : {config.AUDIO_QUALITY}")
        print(f"  28) Audio Format   : {config.DEFAULT_AUDIO_FORMAT}")
        print(f"  29) Sig. Auto Apply: {config.AUDIO_SIGNATURE_AUTO}")
        print(f"  30) Sig. Path      : {config.AUDIO_SIGNATURE_PATH}")
        print(f"  31) Sig. Volume    : {config.AUDIO_SIGNATURE_SIG_VOL}")
        print(f"  32) Main Volume    : {config.AUDIO_SIGNATURE_MAIN_VOL}")
        print(f"  33) Sig. Mode      : {config.AUDIO_SIGNATURE_MODE}")
        print(f"  34) Sig. Offset    : {config.AUDIO_SIGNATURE_OFFSET}s")
        print("\n [ 5: SMART CLIP (CLIPPER) ]")
        print(f"  35) Default Mode   : {config.DEFAULT_CLIP_MODE}")
        print(f"  36) Clip Duration  : {config.DEFAULT_CLIP_DURATION}s")
        print(f"  37) Clip Dir Name  : {config.DEFAULT_CLIPS_DIR_NAME}")
        print("\n [ 6: LOGO MOTION ]")
        print(f"  38) Bounce Wait    : {config.LOGO_BOUNCE_WAIT}s")
        print(f"  39) Link to Dur    : {'[YES]' if config.LOGO_BOUNCE_LINKED_TO_DURATION else '[NO]'}")
        print("\n [ 7: WORKFLOW & CLEANING ]")
        print(f"  40) Main Separator : '{config.MAIN_SEPARATOR}'")
        print(f"  41) Tag Separator  : '{config.NAME_SEPARATOR}'")
        print(f"  42) Include Suffix : {'[YES]' if config.INCLUDE_USER_SUFFIX else '[NO]'}")
        print(f"  43) Include Qual.  : {'[YES]' if config.INCLUDE_QUALITY_IN_NAME else '[NO]'}")
        print(f"  44) Clean Words    : {config.REMOVE_WORDS}")
        print(f"  45) Clean Symbols  : {''.join(config.REMOVE_SYMBOLS)}")
        print(f"  46) Auto Preview   : {'[YES]' if config.AUTO_PREVIEW_ORIGINAL else '[NO]'}")
        print("\n [ 8: BASE TEXT (INTRO) ]")
        print(f"  47) Enable BT      : {'[ON]' if config.BASE_TEXT_ENABLED else '[OFF]'}")
        print(f"  48) BT Duration    : {config.BASE_TEXT_DURATION}s")
        print(f"  49) BT Position    : {config.BASE_TEXT_POS}")
        print(f"  50) BT Color       : {config.BASE_TEXT_COLOR}")
        print(f"  51) BT Opacity     : {config.BASE_TEXT_OPACITY}")
        print(f"  52) BT Start Time  : {config.BASE_TEXT_START}s")
        print(f"  53) BT Size Ratio  : {config.BASE_TEXT_SIZE_RATIO}")
        print(f"  54) BT Move Type   : {config.BASE_TEXT_MOVE_TYPE}")
        print(f"  55) BT Loop Count  : {config.BASE_TEXT_APPEAR_COUNT}")
        print("\n [ 9: YOUTUBE STUDIO ]")
        print(f"  56) Download Path  : {config.YOUTUBE_DOWNLOAD_PATH}")
        print(f"  57) Open Folder    : {'[YES]' if config.YOUTUBE_OPEN_FOLDER else '[NO]'}")
        print(f"  58) Finish Sound   : {'[YES]' if config.YOUTUBE_FINISHED_SOUND else '[NO]'}")
        print(f"  59) Smart Naming   : {'[YES]' if config.YOUTUBE_SMART_NAMING else '[NO]'}")
        print("\n [ 10: GLOBAL OUTPUT PATHS ]")
        print(f"  60) Video Out Path : {config.VIDEO_OUTPUT_PATH if config.VIDEO_OUTPUT_PATH else '[None/Local]'}")
        print(f"  61) Audio Out Path : {config.AUDIO_OUTPUT_PATH if config.AUDIO_OUTPUT_PATH else '[None/Local]'}")
        print(f"  62) Clips Out Path : {config.GLOBAL_CLIPS_OUTPUT_PATH if config.GLOBAL_CLIPS_OUTPUT_PATH else '[None/Local]'}")
        print("\n [ 11: SYSTEM CORE ]")
        print(f"  63) Assets Dir     : {config.CORE_ASSETS_DIR}")
        print(f"  64) Poster Path    : {config.CORE_POSTER_PATH}")
        print(f"  65) CPU Priority   : {config.CPU_PRIORITY}")
        print(f"  66) Font Path      : {config.DEFAULT_FONT_PATH}")
        print(f"  67) Finish Alert   : {'[ON]' if config.FINISH_SOUND_ALERT else '[OFF]'}")
        print(f"  68) CPU Sidebar    : {'[ON]' if getattr(config, 'AUTO_OPEN_CPU_MONITOR', False) else '[OFF]'}")
        print("-" * 75)
        print(" [B] Back to Launcher")
        choice = smart_input("\n ► Selection (1-68) or [S]: ").upper()
        if choice == '__BACK__' or not choice: break
        if choice == 'S':
            import_metadata_from_file()
            continue
        if choice == '1': 
            v = smart_input("URL: ")
            if v == '__BACK__': continue
            config.COMPANY_URL = v or config.COMPANY_URL
        elif choice == '2': 
            v = smart_input("Branding: ")
            if v == '__BACK__': continue
            config.BRANDING_TEXT = v or config.BRANDING_TEXT
        elif choice == '3': 
            v = smart_input("Logo Path: ")
            if v == '__BACK__': continue
            config.CORE_LOGO_PATH = v or config.CORE_LOGO_PATH
        elif choice == '4': 
            v = smart_input("Suffix: ")
            if v == '__BACK__': continue
            config.FILE_SUFFIX = v or config.FILE_SUFFIX
        elif choice == '5':
            v = smart_input("Title: ")
            if v == '__BACK__': continue
            config.TITLE = v
        elif choice == '6':
            v = smart_input("Artist: ")
            if v == '__BACK__': continue
            config.ARTIST = v
        elif choice == '7':
            v = smart_input("Album: ")
            if v == '__BACK__': continue
            config.ALBUM_NAME = v
        elif choice == '8':
            v = smart_input("Year: ")
            if v == '__BACK__': continue
            config.DATE_YEAR = v
        elif choice == '9':
            v = smart_input("Track #: ")
            if v == '__BACK__': continue
            config.TRACK_NUMBER = v
        elif choice == '10':
            v = smart_input("Genre: ")
            if v == '__BACK__': continue
            config.GENRE = v
        elif choice == '11':
            v = smart_input("Composer: ")
            if v == '__BACK__': continue
            config.COMPOSER = v
        elif choice == '12':
            v = smart_input("Album Artist: ")
            if v == '__BACK__': continue
            config.ALBUM_ARTIST = v
        elif choice == '13':
            v = smart_input("Comment: ")
            if v == '__BACK__': continue
            config.COMMENT = v
        elif choice == '14':
            v = smart_input("Meta.txt Path: ")
            if v == '__BACK__': continue
            config.METADATA_TEXT_PATH = v or config.METADATA_TEXT_PATH
        elif choice == '15': config.GLOBAL_AUTO_METADATA = not config.GLOBAL_AUTO_METADATA
        elif choice == '16':
            v = smart_input("Res: ")
            if v == '__BACK__': continue
            config.DEFAULT_RESOLUTION = v or config.DEFAULT_RESOLUTION
        elif choice == '17':
            v = smart_input("Bitrate: ")
            if v == '__BACK__': continue
            config.DEFAULT_BITRATE = v or config.DEFAULT_BITRATE
        elif choice == '18':
            v = smart_input("FPS: ")
            if v == '__BACK__': continue
            if v.isdigit(): config.DEFAULT_FPS = int(v)
        elif choice == '19':
            v = smart_input("Blur: ")
            if v == '__BACK__': continue
            config.BLUR_INTENSITY = v or config.BLUR_INTENSITY
        elif choice == '20':
            v = smart_input("Text Color: ")
            if v == '__BACK__': continue
            config.DEFAULT_TEXT_COLOR = v or config.DEFAULT_TEXT_COLOR
        elif choice == '21':
            v = smart_input("Text Size Ratio: ")
            if v == '__BACK__': continue
            if v.isdigit(): config.DEFAULT_TEXT_RATIO = int(v)
        elif choice == '22': config.IGNORE_LOWER_QUALITY = not config.IGNORE_LOWER_QUALITY
        elif choice == '23': config.IGNORE_EQUAL_QUALITY = not config.IGNORE_EQUAL_QUALITY
        elif choice == '24': config.SAVE_CENSOR_CUTS = not config.SAVE_CENSOR_CUTS
        elif choice == '25': config.OVERWRITE_ORIGINAL = not config.OVERWRITE_ORIGINAL
        elif choice == '26': config.RENAME_ORIGINAL_ON_ALL = not config.RENAME_ORIGINAL_ON_ALL
        elif choice == '27':
            v = smart_input("Audio Quality: ")
            if v == '__BACK__': continue
            config.AUDIO_QUALITY = v or config.AUDIO_QUALITY
        elif choice == '28':
            v = smart_input("Format: ")
            if v == '__BACK__': continue
            config.DEFAULT_AUDIO_FORMAT = v or config.DEFAULT_AUDIO_FORMAT
        elif choice == '29': config.AUDIO_SIGNATURE_AUTO = get_choice("Auto Sig?", ["Yes", "No"], default=config.AUDIO_SIGNATURE_AUTO)
        elif choice == '30':
            v = smart_input("Sig Path: ")
            if v == '__BACK__': continue
            config.AUDIO_SIGNATURE_PATH = v or config.AUDIO_SIGNATURE_PATH
        elif choice == '31':
            v = smart_input("Sig Vol: ")
            if v == '__BACK__': continue
            if v: config.AUDIO_SIGNATURE_SIG_VOL = float(v)
        elif choice == '32':
            v = smart_input("Main Vol: ")
            if v == '__BACK__': continue
            if v: config.AUDIO_SIGNATURE_MAIN_VOL = float(v)
        elif choice == '33': config.AUDIO_SIGNATURE_MODE = get_choice("Mode:", ["Start", "End", "Both"], default=config.AUDIO_SIGNATURE_MODE)
        elif choice == '34':
            v = smart_input("Offset: ")
            if v == '__BACK__': continue
            if v.isdigit(): config.AUDIO_SIGNATURE_OFFSET = int(v)
        elif choice == '35': config.DEFAULT_CLIP_MODE = get_choice("Clip Mode:", ["Range", "Random"], default=config.DEFAULT_CLIP_MODE)
        elif choice == '36':
            v = smart_input("Clip Dur: ")
            if v == '__BACK__': continue
            if v.isdigit(): config.DEFAULT_CLIP_DURATION = int(v)
        elif choice == '37':
            v = smart_input("Clip Dir Name: ")
            if v == '__BACK__': continue
            config.DEFAULT_CLIPS_DIR_NAME = v or config.DEFAULT_CLIPS_DIR_NAME
        elif choice == '38':
            v = smart_input("Wait: ")
            if v == '__BACK__': continue
            config.LOGO_BOUNCE_WAIT = v or config.LOGO_BOUNCE_WAIT
        elif choice == '39': config.LOGO_BOUNCE_LINKED_TO_DURATION = not config.LOGO_BOUNCE_LINKED_TO_DURATION
        elif choice == '40':
            v = smart_input("Main Sep: ")
            if v == '__BACK__': continue
            config.MAIN_SEPARATOR = v or config.MAIN_SEPARATOR
        elif choice == '41':
            v = smart_input("Tag Sep: ")
            if v == '__BACK__': continue
            config.NAME_SEPARATOR = v or config.NAME_SEPARATOR
        elif choice == '42': config.INCLUDE_USER_SUFFIX = not config.INCLUDE_USER_SUFFIX
        elif choice == '43': config.INCLUDE_QUALITY_IN_NAME = not config.INCLUDE_QUALITY_IN_NAME
        elif choice == '44':
            print(f"\n [!] Current Words: {config.REMOVE_WORDS}")
            print(" [💡] How to use:")
            print("  • Text only (word1, word2) -> Overwrite entire list")
            print("  • Use (+) to add          -> (+4K, +HD)")
            print("  • Use (-) to remove       -> (-word1, -word2)")
            v = smart_input("\n ► Action: ")
            if v == '__BACK__': continue
            if not v: continue
            
            if '+' not in v and '-' not in v:
                # Overwrite mode
                config.REMOVE_WORDS = [w.strip() for w in v.split(',') if w.strip()]
            else:
                # Incremental mode (+ or -)
                parts = [p.strip() for p in v.split(',') if p.strip()]
                for p in parts:
                    if p.startswith('+'):
                        word = p[1:].strip()
                        if word and word not in config.REMOVE_WORDS: config.REMOVE_WORDS.append(word)
                    elif p.startswith('-'):
                        word = p[1:].strip()
                        config.REMOVE_WORDS = [w for w in config.REMOVE_WORDS if w != word]
                    else:
                        # Default to add if no prefix but other parts have them? 
                        # Or just ignore. Let's assume user error and ignore prefixless in mixed mode.
                        pass
        elif choice == '45':
            print(f"\n [!] Current Symbols: {''.join(config.REMOVE_SYMBOLS)}")
            print(" [💡] Use (+), (-) or text only to overwrite.")
            v = smart_input("\n ► Action: ")
            if v == '__BACK__': continue
            if not v: continue
            
            if '+' not in v and '-' not in v:
                config.REMOVE_SYMBOLS = list(v)
            else:
                parts = [p.strip() for p in v.split(',') if p.strip()]
                if len(parts) == 1 and (v.startswith('+') or v.startswith('-')):
                    # Special case for symbols: if they didn't use commas (e.g. +!@#)
                    prefix = v[0]
                    syms = v[1:]
                    for s in syms:
                        if prefix == '+':
                            if s not in config.REMOVE_SYMBOLS: config.REMOVE_SYMBOLS.append(s)
                        else:
                            config.REMOVE_SYMBOLS = [x for x in config.REMOVE_SYMBOLS if x != s]
                else:
                    for p in parts:
                        if p.startswith('+'):
                            s_val = p[1:].strip()
                            for s in s_val:
                                if s not in config.REMOVE_SYMBOLS: config.REMOVE_SYMBOLS.append(s)
                        elif p.startswith('-'):
                            s_val = p[1:].strip()
                            for s in s_val:
                                config.REMOVE_SYMBOLS = [x for x in config.REMOVE_SYMBOLS if x != s]
        elif choice == '46': config.AUTO_PREVIEW_ORIGINAL = not config.AUTO_PREVIEW_ORIGINAL
        elif choice == '47': config.BASE_TEXT_ENABLED = not config.BASE_TEXT_ENABLED
        elif choice == '48':
            v = smart_input("BT Dur: ")
            if v == '__BACK__': continue
            if v: config.BASE_TEXT_DURATION = float(v)
        elif choice == '49':
            config.BASE_TEXT_POS = get_choice("Pos:", [
                "Top-Left", "Top-Center", "Top-Right",
                "Middle-Left", "Center", "Middle-Right",
                "Bottom-Left", "Bottom-Center", "Bottom-Right"
            ], default=config.BASE_TEXT_POS)
        elif choice == '50':
            v = smart_input("BT Color: ")
            if v == '__BACK__': continue
            config.BASE_TEXT_COLOR = v or config.BASE_TEXT_COLOR
        elif choice == '51':
            v = smart_input("BT Opacity: ")
            if v == '__BACK__': continue
            if v: config.BASE_TEXT_OPACITY = float(v)
        elif choice == '52':
            v = smart_input("Start: ")
            if v == '__BACK__': continue
            if v.isdigit(): config.BASE_TEXT_START = int(v)
        elif choice == '53':
            v = smart_input("Size Ratio: ")
            if v == '__BACK__': continue
            if v.isdigit(): config.BASE_TEXT_SIZE_RATIO = int(v)
        elif choice == '54':
            config.BASE_TEXT_MOVE_TYPE = get_choice("Move:", ["None", "L-R", "R-L", "T-B", "B-T"], default=config.BASE_TEXT_MOVE_TYPE)
        elif choice == '55':
            v = smart_input("Loop Count: ")
            if v == '__BACK__': continue
            if v.isdigit(): config.BASE_TEXT_APPEAR_COUNT = int(v)
        elif choice == '56':
            v = smart_input("YT Path: ")
            if v == '__BACK__': continue
            config.YOUTUBE_DOWNLOAD_PATH = v or config.YOUTUBE_DOWNLOAD_PATH
        elif choice == '57': config.YOUTUBE_OPEN_FOLDER = not config.YOUTUBE_OPEN_FOLDER
        elif choice == '58': config.YOUTUBE_FINISHED_SOUND = not config.YOUTUBE_FINISHED_SOUND
        elif choice == '59': config.YOUTUBE_SMART_NAMING = not config.YOUTUBE_SMART_NAMING
        elif choice == '60':
            v = smart_input("Video Out Path: ")
            if v == '__BACK__': continue
            config.VIDEO_OUTPUT_PATH = v or config.VIDEO_OUTPUT_PATH
        elif choice == '61':
            v = smart_input("Audio Out Path: ")
            if v == '__BACK__': continue
            config.AUDIO_OUTPUT_PATH = v or config.AUDIO_OUTPUT_PATH
        elif choice == '62':
            v = smart_input("Clips Out Path: ")
            if v == '__BACK__': continue
            config.GLOBAL_CLIPS_OUTPUT_PATH = v or config.GLOBAL_CLIPS_OUTPUT_PATH
        elif choice == '63':
            v = smart_input("Assets Dir: ")
            if v == '__BACK__': continue
            config.CORE_ASSETS_DIR = v or config.CORE_ASSETS_DIR
        elif choice == '64':
            v = smart_input("Poster Path: ")
            if v == '__BACK__': continue
            config.CORE_POSTER_PATH = v or config.CORE_POSTER_PATH
        elif choice == '65':
            config.CPU_PRIORITY = get_choice("Priority:", ["Idle", "BelowNormal", "Normal", "High"], default=config.CPU_PRIORITY)
        elif choice == '66':
            v = smart_input("Font Path: ")
            if v == '__BACK__': continue
            config.DEFAULT_FONT_PATH = v or config.DEFAULT_FONT_PATH
        elif choice == '67': config.FINISH_SOUND_ALERT = not config.FINISH_SOUND_ALERT
        elif choice == '68': config.AUTO_OPEN_CPU_MONITOR = not getattr(config, 'AUTO_OPEN_CPU_MONITOR', False)
        save_all_to_config()