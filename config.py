import os

COMPANY_URL = "@sabagroupye"
BRANDING_TEXT = "مجموعة سبأ للخدمات الإعلانية"
TITLE = "SABAGROUP"
ARTIST = "Saba Group"
ALBUM_NAME = "Saba Group Media Production"
GENRE = "مجموعة سبأ للخدمات الإعلانية والإعلامية وخدمات التسويق والتطوير"
COMPOSER = "مجموعة سبأ للخدمات الإعلانية والإعلامية وخدمات التسويق والتطوير"
COMMENT = "مجموعة سبأ للخدمات الإعلانية والإعلامية وخدمات التسويق والتطوير"
ALBUM_ARTIST = "مجموعة سبأ للخدمات الإعلانية والإعلامية وخدمات التسويق والتطوير"
DATE_YEAR = "مجموعة سبأ للخدمات الإعلانية والإعلامية وخدمات التسويق والتطوير"
TRACK_NUMBER = "مجموعة سبأ للخدمات الإعلانية والإعلامية وخدمات التسويق والتطوير"

# Dynamic cross-platform base directories
if os.name == 'nt':
    CORE_ASSETS_DIR = r"C:\SGAM_STMedia"
    VIDEO_OUTPUT_PATH = r"C:\SGAM_VIDEO_OUTPUT"
    AUDIO_OUTPUT_PATH = r"C:\SGAM_AUDIO_OUTPUT"
    GLOBAL_CLIPS_OUTPUT_PATH = r"C:\SGAM_CLIPS_SAVE"
    YOUTUBE_DOWNLOAD_PATH = r"C:\SGAM_Youtube"
else:
    # macOS / Linux: Place inside user's home directory
    CORE_ASSETS_DIR = os.path.expanduser("~/SGAM_STMedia")
    VIDEO_OUTPUT_PATH = os.path.expanduser("~/SGAM_VIDEO_OUTPUT")
    AUDIO_OUTPUT_PATH = os.path.expanduser("~/SGAM_AUDIO_OUTPUT")
    GLOBAL_CLIPS_OUTPUT_PATH = os.path.expanduser("~/SGAM_CLIPS_SAVE")
    YOUTUBE_DOWNLOAD_PATH = os.path.expanduser("~/SGAM_Youtube")

METADATA_TEXT_PATH = r"C:\SGAM_STMedia\metadata.txt"
CORE_LOGO_PATH = r"C:\SGAM_STMedia\sg_logo_video.png"
CORE_POSTER_PATH = r"C:\SGAM_STMedia\poster.jpg"
AUDIO_SIGNATURE_PATH = r"C:\SGAM_STMedia\remix audio.mp3"
DEFAULT_FONT_PATH = r"C:\SGAM_STMedia\ge-hili-book.otf"

OVERWRITE_ORIGINAL = False
RENAME_ORIGINAL_ON_ALL = False
FILE_SUFFIX = "مجموعة سبأ"
MAIN_SEPARATOR = " | "
NAME_SEPARATOR = "_"
INCLUDE_USER_SUFFIX = True
INCLUDE_QUALITY_IN_NAME = True

REMOVE_WORDS = ['HD', 'SD', 'MP4', 'MP3', '720p', '1080p', '480p', '360p', '240p', 'YouTube', '1080', '480', '360', '240', '2K', '4K', 'K2', 'K4', 'مستر نت', 'مسترنت', 'زيزو نت', 'زيزونت']

REMOVE_SYMBOLS = ['|', '\\', ':', '"', '<', '>', '?', '/', '$', '#', '&', '@', '*', '%', '^', '(', ')', '{', '}', '[', ']', ';', "'", ',', '.', '~', '+', '=', '`', '°']

DEFAULT_RESOLUTION = "720p"
DEFAULT_BITRATE = "1500k"
DEFAULT_FPS = 25
BLUR_INTENSITY = "25:10"
DEFAULT_TEXT_COLOR = "white"
DEFAULT_TEXT_RATIO = 20

BASE_TEXT_ENABLED = True
BASE_TEXT_COLOR = "white"
BASE_TEXT_OPACITY = 0.9
BASE_TEXT_SIZE_RATIO = 20
BASE_TEXT_START = 0
BASE_TEXT_DURATION = 15
BASE_TEXT_POS = "Bottom-Center"
BASE_TEXT_MOVE_TYPE = "None"
BASE_TEXT_APPEAR_COUNT = 1

AUDIO_QUALITY = "320k"
DEFAULT_AUDIO_FORMAT = "mp3"
AUDIO_SIGNATURE_AUTO = "No"
AUDIO_SIGNATURE_MODE = "Both"
AUDIO_SIGNATURE_OFFSET = 5
AUDIO_SIGNATURE_MAIN_VOL = 0.5
AUDIO_SIGNATURE_SIG_VOL = 0.7

DEFAULT_CLIP_MODE = "Range"
DEFAULT_CLIP_DURATION = 30
DEFAULT_CLIPS_DIR_NAME = "SG_CLIPS"
CPU_PRIORITY = "Normal"
FINISH_SOUND_ALERT = True

AUTO_OPEN_CPU_MONITOR = False
IGNORE_LOWER_QUALITY = True
IGNORE_EQUAL_QUALITY = False
GLOBAL_AUTO_METADATA = True
AUTO_PREVIEW_ORIGINAL = True
SAVE_CENSOR_CUTS = True
LOGO_BOUNCE_WAIT = "10"
LOGO_BOUNCE_LINKED_TO_DURATION = True

# YOUTUBE_DOWNLOAD_PATH is defined dynamically above
YOUTUBE_OPEN_FOLDER = True
YOUTUBE_FINISHED_SOUND = True
YOUTUBE_SMART_NAMING = True
