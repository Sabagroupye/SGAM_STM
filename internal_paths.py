import os
import config as config

# --- BASE SYSTEM PATHS ---
BASE_INPUT = config.CORE_ASSETS_DIR
CORE_ASSETS_DIR = BASE_INPUT  

# --- VIDEO ASSETS ---
CORE_LOGO = config.CORE_LOGO_PATH
CORE_POSTER = config.CORE_POSTER_PATH
CORE_TEXTS = os.path.join(BASE_INPUT, "texts.txt")

# --- EXECUTABLES ---
FFMPEG_FOLDER = BASE_INPUT
CORE_FFMPEG = os.path.join(BASE_INPUT, "ffmpeg.exe")
CORE_FFPROBE = os.path.join(BASE_INPUT, "ffprobe.exe")