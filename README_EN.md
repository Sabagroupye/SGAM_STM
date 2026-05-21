# 🚀 SGAM STMEDIA v1.26 | The Comprehensive Technical Encyclopedia

This guide is the official and integrated technical reference for the **SGAM STMEDIA** system, designed and developed by **SABA GROUP**. This documentation aims to provide a "microscopic" view of every corner of the system, starting from the file infrastructure to the most complex video and audio processing algorithms.

---

## 🏗️ Part 1: Programming Architecture & "Batch" Components Detail

The **SGAM STMEDIA** system relies on a "Modular Architecture," where the system is divided into a group of specialized programming files that work in perfect harmony. This division ensures processing speed, ease of maintenance, and the stability of the "Batch" when dealing with thousands of files.

### 1.1 Core Operation & Central Control Files (Core & Boot Files)

These files form the "Brain" that drives the system, responsible for starting operations and adjusting the technical environment:

*   **`launcher.py` (Main Launcher):**
    *   **Function:** It is the only entry point to the system. It starts the program lifecycle and calls the environment verification engine.
    *   **Programming Logic:** Contains the "Main Dispatcher" that monitors the user interface and waits for "Drag and Drop" operations. It is responsible for linking Video, Audio, and YouTube centers.
    *   **Links:** Calls `dependency_manager.py`, `utils.py`, and `settings_ui.py`.

*   **`reception_hub.py` (Smart Reception Center):**
    *   **Function:** Acts as a smart "receptionist." When the user drags a group of mixed files (Video + Audio + Folders), this file analyzes and categorizes them.
    *   **Programming Logic:** Uses the `shlex` and `re` (Regex) libraries to analyze complex paths resulting from dragging files in a Windows environment, and decides to direct the user to "Video Processing," "Audio Processing," or "Batch Renaming."

*   **`utils.py` (Comprehensive Tool Library):**
    *   **Function:** The largest file in the system, containing all shared functions (Utility Functions).
    *   **Programming Logic:** Includes basic rendering functions, metadata extraction functions, screen cleaning, and aesthetic report header generation. Any repetitive process in the system is called from this file to ensure performance unity.

*   **`dependency_manager.py` (System Guardian):**
    *   **Function:** Ensures that the user's device is fully ready for work.
    *   **Programming Logic:** Checks the Python version, verifies the presence of the `ffmpeg.exe` engine locally or globally, and checks programming libraries such as `yt-dlp` and `mutagen`. If there is a shortage, it requests automatic installation via `pip`.

*   **`cpu_controller.py` (Processor Resource Organizer):**
    *   **Function:** Controls the "strength" of the system's consumption of computer resources.
    *   **Programming Logic:** Uses the `psutil` library to raise or lower the priority of rendering processes. It allows the user to work on other programs while the batch is running without causing "slowness" in the device.

---

### 1.2 Video Production Modules

These files are responsible for processing images, videos, and layers:

*   **`video_pro.py` (Video Production Manager):**
    *   **Function:** Controls the workflow for video operations.
    *   **Programming Logic:** Contains the seven menus for video production and manages storage strategies (Local, Mirror, or Global folder).

*   **`video_logic.py` (Video Brain):**
    *   **Function:** Converts user choices into programming commands understood by the FFmpeg engine.
    *   **Programming Logic:** Builds the complex "Filter Complex" chain that merges the logo with censoring and text layers into one unified command.

*   **`editor.py` (Visual Layer Editor):**
    *   **Function:** Processes texts and logos.
    *   **Programming Logic:** Contains algorithms for calculating the (x, y) coordinates of the moving logo (Dynamic Bounce) and text locations based on video resolution (720p, 1080p, etc.).

*   **`censor.py` and `censor_ui.py` (Censorship System):**
    *   **Function:** Manages blocking operations (Blur, Freeze, Cut).
    *   **Programming Logic:** Controls "Time Cutting" and "Visual Blurring," and allows the user to preview the file before making a blocking decision.

*   **`video_card_pro.py` (Video Card Designer):**
    *   **Function:** An interface for creating and editing video templates.
    *   **Programming Logic:** Allows the user to program templates containing specific sizes, logo locations, and pre-set animated text layers.

---

### 1.3 Audio Production Modules

*   **`audio_pro.py` (Audio Production Manager):**
    *   **Function:** Manages batches of audio files, conversion, and clipping processes.
    *   **Programming Logic:** Manages the four audio production modes and controls drag-and-drop operations for audio.

*   **`audio_logic.py` (Digital Audio Engineer):**
    *   **Function:** Executes mixing and merging processes.
    *   **Programming Logic:** Builds commands to merge the audio signature with the main material while considering volume levels (Volume Ducking).

*   **`audio_card_pro.py` (Audio Card Designer):**
    *   **Function:** Saves mixing and audio quality settings.
    *   **Programming Logic:** Allows for the creation of custom templates for each audio "brand" including bitrate and encoding type.

---

### 1.4 Metadata & Tagging Modules

*   **`metadata.py` and `fast_meta_pro.py`:**
    *   **Function:** Inject metadata (ID3 & XMP) and cover images.
    *   **Programming Logic:** Uses the `mutagen` library to write artist, album, and genre data into files without the need for re-rendering, preserving the original quality.

*   **`tag_logic.py` (Smart Tagging Engine):**
    *   **Function:** Building professional filenames.
    *   **Programming Logic:** Ensures that the **(SGAM)** tag remains mandatory in the name, and merges quality, suffix, and the original name using the separators defined in the settings.

---

### 1.5 Auxiliary Systems & Downloaders

*   **`youtube_downloader.py` (Professional YouTube Downloader):**
    *   **Function:** Download content from the internet in high qualities.
    *   **Programming Logic:** Uses the `yt-dlp` engine with the integration of a "Queue" system to download multiple links sequentially, with mandatory identity enforcement immediately after downloading.

*   **`renamer_pro.py` (Smart Renaming):**
    *   **Function:** Modifying filenames collectively.
    *   **Programming Logic:** Executes search and replace operations, adds prefixes and suffixes, and cleans names of impurities.

*   **`folder_pro.py` (Folders & Structure Manager):**
    *   **Function:** Processing folder structure.
    *   **Programming Logic:** Manages "Mirroring" options and cleans subfolder names to ensure a clean archival order.

*   **`converter.py` (Format & Encoding Converter):**
    *   **Function:** Controls encoding standards.
    *   **Programming Logic:** Contains the quality matrix (240p, 480p, 720p, 1080p) and appropriate bitrates for each.

*   **`SGAM_BACKUP_MANAGER.py` (Backup System):**
    *   **Function:** Protects system assets.
    *   **Programming Logic:** Performs periodic backups of settings and presets to ensure they are not lost in the event of a device error.

---

### 1.6 Configuration & Paths Files

*   **`config.py` (System DNA):**
    *   **Function:** Storing all fixed and variable settings.
    *   **Content:** Includes more than 100 technical variables, including (company links, default identity, quality settings, prohibited words in naming, and global save paths).
    *   **Importance:** Any modification in this file is immediately reflected in the behavior of the entire batch.

*   **`internal_paths.py` (Internal Paths Manager):**
    *   **Function:** Unifying access addresses to attachments.
    *   **Content:** Ensures that all programming files know the location of (logos, fonts, posters, and audio signatures) in the main folder `C:\SGAM_STMedia`.

*   **`settings_manager.py` (Presets Manager):**
    *   **Function:** Managing save and read operations for settings cards (Presets).
    *   **Programming Logic:** Converts user choices into `JSON` files or updates them within `presets.json` to ensure they remain even after the program is closed.

---

### 1.7 Auxiliary Support Files

*   **`START_SGAM.bat`:**
    *   **Function:** A quick one-click executable file.
    *   **Content:** Starts the Python environment and directs it to the `launcher.py` file directly, sparing the user from dealing with the command line (CMD).

*   **`sgam_process_log.txt`:**
    *   **Function:** The system's black box.
    *   **Content:** Records every command executed, every error that occurred, and the start and end timing of each "render" process.

---

**Technical Note:** These files were designed to be "Loose Coupling, High Cohesion," preventing the entire system from collapsing in the event of an error in one part, and allowing the batch to continue processing the rest of the files successfully.

---

## 🎬 Part 2: Video Processing Hub

The "Video Processing Hub" is the heart of the **SGAM STMEDIA** system, designed to be a comprehensive solution that combines extreme automation with precise control over video output. The hub relies on the advanced **FFmpeg** engine to execute complex processing chains that ensure quality remains at its highest levels.

### 2.1 The Seven Operation Modes

When dragging video files into the system, the user is given a choice between 7 specialized programming modes:

1.  **🚀 FULL SYSTEM:**
    *   **Process:** Executing the complete production cycle (Inserting Logo + Censoring Scenes + Improving Quality + Injecting Metadata + Adding Mandatory Suffixes).
    *   **Usage:** Used to produce raw materials and convert them into final materials ready for publishing with a single click.

2.  **🎨 EDIT ONLY Mode:**
    *   **Process:** Focusing on visual identity (Inserting Logo + Text Layers + Metadata).
    *   **Usage:** Ideal for materials that do not need censorship or blocking, but only need documentation of identity and rights.

3.  **✂️ CENSOR ONLY Mode:**
    *   **Process:** Processing censorial content (Blocking/Cutting) with metadata injection.
    *   **Usage:** Used to purify sensitive content with extreme speed while maintaining the original video characteristics.

4.  **🏷️ METADATA ONLY Mode:**
    *   **Process:** Injecting album, artist, featuring artist, composer, and poster data.
    *   **Feature:** This process takes "fractions of a second" because it does not re-render the video (No Re-encoding), but rather modifies the file headers (Header Injection).

5.  **✨ QUALITY + META Mode:**
    *   **Process:** Changing video dimensions (720p, 1080p, etc.) and bitrate with data injection.
    *   **Usage:** To unify the dimensions of large batches of videos from different sources.

6.  **🎞️ QUALITY ONLY Mode:**
    *   **Process:** Changing resolution and encoding only.
    *   **Usage:** For pure technical conversion without adding any tags or logos.

7.  **🎵 EXTRACT AUDIO:**
    *   **Process:** Converting video into a high-quality audio file (MP3/M4A).
    *   **Feature:** The system automatically detects the best bitrate for the original audio and extracts it while injecting video metadata into the resulting audio file.

---

### 2.2 Advanced Censorship & Blocking System

The system provides three programming modes for dealing with unwanted scenes:

*   **Freeze Frame:** The system freezes a specific frame on the screen while the original audio continues to flow. Useful for hiding quick shots without cutting the audio sequence.
*   **Blur/Mosaic:** Applying high-resolution blurring to the selected scene. "Blur Intensity" can be controlled from global settings.
*   **Cut Mode:** Removing the scene entirely from the video timeline.
    *   **Keep Mode Feature:** Allows the user to specify "what they want to keep" only, and the system will delete everything else, which is the fastest pattern for gathering important clips from long videos.

---

### 2.3 Layering & Logo Dynamics System

The system is characterized by a superior ability to manage visual elements over the video:

*   **Static Logo:** Placing the institution's logo in 9 strategic positions (Top-Right, Bottom-Left, etc.).
*   **Dynamic Bounce Technique:** To prevent screen recording or logo removal by AI, the system moves the logo between the corners of the screen in programmed time intervals.
*   **Animated Text Layers:** Support for adding animated texts (L-R, R-L, T-B, B-T) with control over font color, size, and opacity.

---

### 2.4 Output & Saving Strategies

The system supports 3 smart ways to organize produced files:

1.  **Global Output Folder:** Saving all outputs in a single central path (e.g., `C:\SGAM_VIDEO_OUTPUT`).
2.  **Local Mode:** Saving the modified file in the same folder as the original file.
3.  **Full Mirroring:** This is the most powerful feature; where the system completely reconstructs the original folder tree within the output folder, moving non-media files (images, texts) as they are to ensure that archival order is not lost.

---

**Programming Note:** The system relies on "Smart Encoding" in its video production; where the original video is checked, and if its quality is lower than the selected quality, the system warns the user or skips the file to maintain the professional standards of the institution.

---

## 🎵 Part 3: Audio Processing Hub

The "Audio Processing Hub" is an advanced system for collective digital audio engineering, providing precise tools for dealing with audio files with studio quality. The system is designed to integrate audio branding and protect rights while maintaining the purity of the original material.

### 3.1 The Four Audio Operation Modes

The Audio Hub provides 4 dedicated processing paths:

1.  **🚀 FULL PRODUCTION:**
    *   **Process:** Comprehensive audio processing including (Quality Adjustment + Audio Signature Merging + Full Metadata Injection + Cover Image).
    *   **Feature:** The system automatically performs a professional mix that ensures the institution's audio signature appears clearly over the main material.

2.  **🔄 CONVERT/TRANSCODE:**
    *   **Process:** Changing the file format (e.g., from WAV to MP3) or changing the bitrate.
    *   **Options:** You can choose between keeping the original quality or converting to a specific quality via "Audio Cards."

3.  **✂️ SMART CLIP:**
    *   **Process:** Extracting specific parts from long audio files.
    *   **Patterns:**
        *   **Range Mode:** Extracting a clip with a specific start and end time.
        *   **Random Sample Mode:** The system automatically selects a random clip of a specific length (e.g., 30 seconds) from the middle of the file, which is ideal for creating quick "previews."

4.  **🏷️ METADATA ONLY Mode:**
    *   **Process:** Editing ID3 tags (Title, Artist, Album, Year) and inserting the cover image.
    *   **Feature:** The process takes place at extreme speed without re-encoding the audio, ensuring "zero" loss in quality.

---

### 3.2 Audio Signature Mixing Engineering

The system uses advanced algorithms to merge audio identity:

*   **Signature Mode:** The signature can be set to appear at (Beginning of clip, End of clip, or both).
*   **Offset:** The ability to specify a precise timing for the start of the signature (e.g., starts after 5 seconds from the beginning of the clip).
*   **Volume Ducking:** The system reduces the volume of the main material by a specific percentage (e.g., 50%) when the audio signature appears, to ensure the clarity of the "Identity" without annoying overlap.

---

### 3.3 Quality Protection & Bitrate Intelligence

*   **Quality Discovery:** The system checks the original bitrate of the file.
*   **Smart Advisor:** If the user tries to convert to a quality higher than the original (Upscaling), the system skips the file or warns the user; because that will not improve the quality but will only increase the file size without benefit.
*   **Format Support:** The system supports all professional formats including (MP3, WAV, M4A, FLAC, OGG).

---

**Programming Note:** The cover image (Poster/Cover Art) is injected inside the MP3 file professionally, so that the image appears clearly in all international music players, car systems, and smartphones.

---

## 🎴 Part 4: Card Hub & Presets System

The "Card System" is the strategic brain of the **SGAM STMEDIA** system, allowing the producer to build "Production Templates" ready for repeated use. Instead of entering settings every time, you can choose a pre-prepared "card" that executes all complex operations with a single click.

### 4.1 The Professional Video Card

The video card is a miniature factory containing all visual identity standards:

1.  **Quality Specs:**
    *   **Resolution:** Support for all sizes from 240p up to 4K.
    *   **FPS:** Determining the smoothness of movement (e.g., 30fps or 60fps).
    *   **Bitrate:** Controlling the final file size and image clarity.

2.  **Logo Dynamics:**
    *   **Static Positions:** Choosing one of 9 anchor points on the screen.
    *   **Dynamic Bounce Technique:** To prevent content theft, the logo can be programmed to move between corners in a specific sequence (e.g., Top-Right -> Bottom-Left -> Top-Left) in programmed time cycles.
    *   **Transparency & Size:** Full control over the degree of logo appearance and its size relative to the video dimensions.

3.  **Layer Manager System:**
    *   **Relative Timing:** Linking the appearance of the text to a specific moment in time (Beginning, Middle, or End of the video).
    *   **Animation Patterns:**
        *   Support for animation from 4 directions (Left-Right, Right-Left, Top-Bottom, Bottom-Top).
        *   Specifying the movement direction (In / Out).
        *   **Looping:** The ability to repeat the appearance of the animated text throughout the video period.

---

### 4.2 The Audio Card

This card focuses on the quality of the audio output and the strength of the audio identity:

*   **Encoding Settings:** Specifying the output format (MP3/M4A) and preferred bitrate.
*   **Mixing Logic:** Storing audio signature (Signature) merging settings and the appropriate (Ducking) ratio for each brand.

---

### 4.3 Preset Management

The system provides a graphical interface (Designer) to manage these cards with ease:
*   **Add:** Create a new card from scratch.
*   **Edit:** Update an existing card's settings without having to delete it.
*   **Duplicate:** Create a copy of a successful card for minor modifications (e.g., changing quality only).
*   **Delete:** Remove old or unused cards.

---

**Programming Note:** All data for these cards is stored in structurally encrypted (JSON) files within the program folder, ensuring the continuity of settings even when moving the program from one device to another.

---

## 🤖 Part 5: Advanced Automation Systems

The **SGAM STMEDIA** system is characterized by an exceptional ability to "think" for the user in repetitive and boring tasks. Thanks to integrated automation engines, the system can manage, organize, and tag hundreds of files completely automatically.

### 5.1 Renamer Pro Engine

Unlike traditional naming tools, "Renamer Pro" in this system works as a smart system that protects property rights while editing:

1.  **Batch Modification Patterns:**
    *   **Find & Replace:** Replacing specific texts with other texts in hundreds of names at once.
    *   **Prefix:** Adding an introductory text at the beginning of all names.
    *   **Suffix:** Adding an introductory text just before the file extension.
2.  **Scope Control:**
    *   You can choose to execute the process on (Files only, Folders only, or both together).
    *   **Recursion:** The ability to reach subfolders and process their contents completely.
3.  **Mandatory Protection Technique:**
    *   When performing a replacement process, the system monitors the **(SGAM)** tag and hides it in a "protected area" temporarily, then re-injects it into the new name to ensure that rights are not deleted by mistake.
4.  **Cleaning & Final Preparation:**
    *   After finishing the modification, the name passes through the "Cleaning Engine" to delete double spaces, extra symbols, and apply the "Professional Separators" specified in the settings.

---

### 5.2 YouTube Studio Pro Downloader

It is not just a normal download tool, but rather a "Download Manager" linked to the production system:

*   **Multi-Link Queue:** Adding multiple YouTube links and downloading them sequentially without stopping.
*   **Multi-Format & Quality:**
    *   Download video in the highest available quality (4K, 1080p, 720p).
    *   Download "Audio Only" in high-quality MP3 format.
*   **Branding Lock:** Once the video is downloaded, the system immediately enforces systematic naming, deletes long, inconsistent names placed by YouTubers, and adds the mandatory tag.

---

### 5.3 Process Logging & Control

The system provides full transparency and real-time control over ongoing operations:

1.  **Process Log (`sgam_process_log.txt`):**
    *   An external file that is updated in real-time with every step the batch takes.
    *   Shows precise information about the processor, technical errors, and execution timings.
2.  **Process Interrupt:**
    *   The user can monitor render progress in seconds via the interface.
    *   The ability to stop the process at any moment via the `Ctrl+C` shortcut without causing a system hang, with the system cleaning temporary files immediately.
3.  **Performance Tracking:**
    *   The system shows the resource consumption of each process, helping in the decision to raise or lower priority.

---

### 5.4 External Metadata Sync

*   **`metadata.txt` file:** The "Auto-Capture" feature for data from external text files to ensure the unification of album, lecture, and series data.

---

## ⚙️ Part 6: System Control & Config Matrix

The settings system in **SGAM STMEDIA** is the central control panel that gives the user full control over more than 60 technical variables. Settings are divided into 11 organized categories for ease of access and modification.

### 6.1 Configuration Categories (The Matrix)

#### **1. Identity & Branding:**
*   **Company URL:** The official link that appears in the metadata.
*   **Branding Text:** The fixed introductory text of the institution.
*   **Core Logo Path:** The reference path for the institution's logo (PNG).
*   **Filename Suffix:** The systematic suffix added to all produced files.

#### **2. Metadata Engine:**
*   **Global Fields:** Setting (Title, Artist, Album, Year, Genre, Composer) by default for all files.
*   **AutoMeta:** Enabling or disabling automatic data injection during rendering.
*   **Sync from metadata.txt:** The professional feature to fetch data from external text files with a single click.

#### **3. Video Engine:**
*   **Resolution & FPS:** Setting the default resolution and frame rate (e.g., 1080p @ 30fps).
*   **Bitrate Logic:** Determining the data flow rate to ensure balance between size and quality.
*   **Blur Intensity:** Controlling the intensity of scene blocking.
*   **Quality Guard:** (Ignore Lower Quality) options to prevent rendering at a quality higher than the original, protecting from wasting time on poor files.

#### **4. Audio Engine:**
*   **Audio Quality:** Setting the audio bitrate (e.g., 192k or 320k).
*   **Signature Mix:** Controlling the volume levels of the signature (Sig Volume) against the main material (Main Volume).
*   **Sig Offset:** Specifying silence periods or delays before the audio signature starts.

#### **5. Smart Clipper:**
*   **Clip Duration:** Specifying the default length for extracted clips.
*   **Clip Mode:** Choosing between manual clipping (Range) or random sample (Random).

#### **6. Logo Motion:**
*   **Bounce Wait:** Specifying the period for the logo to remain in each corner before moving.
*   **Linked to Duration:** Making the logo movement speed linked to the video length (short videos move faster).

#### **7. Workflow & Cleaning:**
*   **Separators:** Choosing separator symbols in filenames (e.g., `_` or `|`).
*   **Clean Lists:** Managing the list of "Prohibited Words" and "Prohibited Symbols" that the system wipes automatically.
*   **Auto Preview:** Opening the original file for preview automatically before processing starts to ensure selection accuracy.

#### **8. Base Text (Intro):**
*   An integrated system for adding a "Text Line" at the beginning of the video including (Content, Location, Color, Opacity, and movement type).

#### **9. YouTube Studio:**
*   Customizing download paths, enabling auto-open folder options after finishing, and enabling "Smart Naming" for downloads.

#### **10. Global Output Paths:**
*   Specifying fixed paths (outside the work folder) to save videos, audios, and clips.

#### **11. System Core:**
*   **CPU Priority:** Controlling the processing rank (Idle, Normal, High) to manage device resources.
*   **Font Path:** Specifying the Arabic/English font used in text layers.

---

### 6.2 Save & Persistence

*   **Real-time Saving:** As soon as any option is modified in the interface, the `config.py` file is updated programmatically immediately.
*   **Protection System:** The system makes a backup copy of the settings to ensure that "lifetime work" in customizing templates and cards is not lost.

---

## 🏁 Official Conclusion

The **SGAM STMEDIA** system is not just a programming tool, but a production partner designed to elevate the standards of Arab media work. With this comprehensive documentation, we put the full power to control your artistic outputs at your fingertips with the highest degrees of accuracy and professionalism.

---

### 🛡️ Ownership & Operation Rights
**All Rights Reserved to Saba Group for Advertising, Marketing, Development & Programming © 2026**
**SABA GROUP FOR ADVERTISING & MARKETING SERVICES**
**Engineering & Development Team | Version 1.26.05**
