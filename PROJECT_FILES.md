# SGAM Media Studio - Project Files Directory

This file serves as a map for the SGAM Media Processor patch. Use it to understand the purpose of each file and ensure organized modifications.

## Core Launcher & UI
- **[launcher.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/launcher.py):** The main entry point for the entire patch. Provides the unified hub menu.
- **[config.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/config.py):** Central configuration for branding, system paths, and processing defaults.
- **[settings_manager.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/settings_manager.py):** Handles loading and saving of presets (cards) in `presets.json`.

## Video Processing
- **[video_pro.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/video_pro.py):** Main runner for batch video production. Manages file selection and processing loops.
- **[video_card_pro.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/video_card_pro.py):** UI for designing and managing Video Cards (resolutions, layers, branding).
- **[video_logic.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/video_logic.py):** Orchestrates the assembly of complex FFmpeg commands for video production.
- **[editor.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/editor.py):** Contains the core FFmpeg filter logic (Logo positioning, text layers, scaling).
- **[censor.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/censor.py):** Implements visual censorship filters like Blur, Freeze, and Cut.

## Audio Processing
- **[audio_pro.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/audio_pro.py):** Main runner for batch audio processing and conversion.
- **[audio_card_pro.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/audio_card_pro.py):** UI for designing Audio Cards (bitrate, format, signature).
- **[audio_logic.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/audio_logic.py):** Handles FFmpeg logic specifically for audio manipulation.

## Specialized Tools
- **[youtube_downloader.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/youtube_downloader.py):** Professional multi-task downloader with smart naming and auto-metadata.
- **[metadata.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/metadata.py):** Core engine for instant metadata injection using Mutagen (MP3/MP4).
- **[fast_meta_pro.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/fast_meta_pro.py):** Standalone tool for batch metadata "Sweep" operations.
- **[converter.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/converter.py):** Quick utility for file format conversions.
- **[extractor.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/extractor.py):** Extracts audio streams from video files.
- **[folder_pro.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/folder_pro.py):** Advanced folder/file management and cleaning utilities.

## Utilities & Internal
- **[utils.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/utils.py):** Common utility functions (path management, smart naming, file sanitization).
- **[cpu_controller.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/cpu_controller.py):** Manages CPU thread priority and system performance.
- **[dependency_manager.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/dependency_manager.py):** Checks and installs required Python libraries.
- **[internal_paths.py](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/internal_paths.py):** Manages system-level file paths (FFmpeg, FFprobe).

## Documentation & Assets
- **[SYSTEM_RULES.md](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/SYSTEM_RULES.md):** The mandatory core logic and rules of the system.
- **[presets.json](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/presets.json):** Data storage for all saved cards.
- **[youtube_queue.json](file:///c:/Users/SABAGROUP%20LAYAN/Desktop/SGAMVID/youtube_queue.json):** Persistent queue for YouTube downloads.

---
*Identity: SGAM Media Studio | @SABAGROUPYE | +967 770574579*
