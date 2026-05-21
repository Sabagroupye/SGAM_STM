import os
import time
import base64
try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, COMM, TXXX, TCOM, TCON, TCOP, TPE2, TDRC, TRCK
    from mutagen.mp4 import MP4, MP4Cover
except ImportError:
    pass 
_CACHED_POSTER_DATA = None
_CACHED_POSTER_PATH = None
def _get_sec_val():
    return base64.b64decode("wqNTR0FNIC0gU2FiYSBHcm91cCB3aHRzIDogKzk2Nzc3MDU3NDU3OQ==").decode('utf-8')
_X_SG_LOCK_ = _get_sec_val()
_X_TAG_CP_ = "cprt"
_X_ID3_CP_ = "TCOP"
from tag_logic import get_system_tag
def get_fast_info(file_path):
    info = {"dur": 0, "bitrate": 0, "w": 0, "h": 0, "quality": "Original"}
    try:
        ext = file_path.lower()
        if ext.endswith('.mp3'):
            audio = MP3(file_path)
            info["dur"] = audio.info.length
            info["bitrate"] = int(audio.info.bitrate / 1000)
            info["quality"] = f"{info['bitrate']}k"
        elif ext.endswith('.mp4'):
            video = MP4(file_path)
            info["dur"] = video.info.length
            info["w"] = getattr(video.info, 'width', 0)
            info["h"] = getattr(video.info, 'height', 0)
            if info["h"] > 0: info["quality"] = f"{info['h']}p"
    except: pass
    return info
def apply_instant_metadata(file_path, poster_path=None):
    global _CACHED_POSTER_DATA, _CACHED_POSTER_PATH
    from config import (
        GLOBAL_AUTO_METADATA, COMPANY_URL, 
        BRANDING_TEXT, ALBUM_NAME, GENRE, COMPOSER, 
        COMMENT, ALBUM_ARTIST, DATE_YEAR, TITLE, ARTIST, TRACK_NUMBER
    )
    from utils import COMPANY_NAME
    if not GLOBAL_AUTO_METADATA: return False
    max_retries = 3
    for attempt in range(max_retries):
        try:
            poster_data = None
            if poster_path and os.path.exists(poster_path):
                if _CACHED_POSTER_PATH == poster_path and _CACHED_POSTER_DATA:
                    poster_data = _CACHED_POSTER_DATA
                else:
                    with open(poster_path, 'rb') as img:
                        poster_data = img.read()
                        _CACHED_POSTER_DATA, _CACHED_POSTER_PATH = poster_data, poster_path
            ext = file_path.lower()
            final_title = TITLE if TITLE else BRANDING_TEXT
            final_artist = ARTIST if ARTIST else COMPANY_NAME
            sys_tag_val = get_system_tag().strip('()')
            if ext.endswith(('.mp3', '.wav')):
                from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, COMM, TXXX, TCOM, TCON, TCOP, TPE2, TDRC, TRCK, ID3NoHeaderError
                try:
                    try: tags = ID3(file_path)
                    except ID3NoHeaderError:
                        tags = ID3()
                        tags.save(file_path)
                        tags = ID3(file_path)
                except:
                    tags = ID3()
                tags["TIT2"] = TIT2(encoding=3, text=final_title)
                tags["TPE1"] = TPE1(encoding=3, text=final_artist)
                tags["TALB"] = TALB(encoding=3, text=ALBUM_NAME)
                tags["COMM"] = COMM(encoding=3, lang='eng', desc='Comment', text=COMMENT)
                tags["TCOM"] = TCOM(encoding=3, text=COMPOSER)
                tags["TCON"] = TCON(encoding=3, text=GENRE)
                tags[_X_ID3_CP_] = TCOP(encoding=3, text=_X_SG_LOCK_)
                tags["TPE2"] = TPE2(encoding=3, text=ALBUM_ARTIST)
                if DATE_YEAR: tags["TDRC"] = TDRC(encoding=3, text=str(DATE_YEAR))
                if TRACK_NUMBER:
                    try: tags["TRCK"] = TRCK(encoding=3, text=str(TRACK_NUMBER))
                    except: pass
                tags.add(TXXX(encoding=3, desc='ProducedBy', text=sys_tag_val))
                if poster_data:
                    tags.delall("APIC")
                    tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=poster_data))
                tags.save(file_path, v2_version=3)
            elif ext.endswith(('.mp4', '.m4a', '.m4v', '.mov')):
                from mutagen.mp4 import MP4, MP4Cover
                video = MP4(file_path)
                video["\xa9nam"] = [final_title]
                video["\xa9ART"] = [final_artist]
                video["\xa9cmt"] = [COMMENT]
                video["\xa9alb"] = [ALBUM_NAME]
                video["\xa9gen"] = [GENRE]
                video[_X_TAG_CP_] = [_X_SG_LOCK_]
                video["\xa9wrt"] = [COMPOSER]
                video["aART"] = [ALBUM_ARTIST]
                if DATE_YEAR: video["\xa9day"] = [str(DATE_YEAR)]
                if TRACK_NUMBER:
                    try:
                        t_num = int(str(TRACK_NUMBER).split('/')[0])
                        video["trkn"] = [(t_num, 0)]
                    except: pass
                video["desc"] = [f"{COMPANY_URL} - {BRANDING_TEXT}"]
                video["purd"] = [sys_tag_val]
                if poster_data:
                    video["covr"] = [MP4Cover(poster_data, imageformat=MP4Cover.FORMAT_JPEG)]
                video.save()
            try:
                os.utime(file_path, None)
                with open(file_path, 'ab') as f:
                    pass 
            except: pass
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(0.4) 
                continue
            if "Permission" in str(e) or "BUSY" in str(e).upper():
                print(f"\n [!] ACCESS DENIED: '{os.path.basename(file_path)}' is BUSY.")
            else:
                print(f"\n [Metadata Error] {os.path.basename(file_path)}: {e}")
    return False