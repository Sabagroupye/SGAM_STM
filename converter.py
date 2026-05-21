def get_converter_args(quality="720p", source_h=None, custom_fps=None, custom_v_bitrate=None, custom_a_bitrate=None):
    presets = {
        "360p": {"w": 640, "h": 360, "v_bit": "500k"},
        "480p": {"w": 854, "h": 480, "v_bit": "800k"},
        "720p": {"w": 1280, "h": 720, "v_bit": "1500k"}
    }
    config = presets.get(quality, presets["720p"])
    target_h = config["h"]
    if source_h and source_h < target_h:
        final_h = source_h
        final_w = -2 
        v_bit = custom_v_bitrate if custom_v_bitrate else "800k" 
    else:
        final_h = target_h
        final_w = config["w"]
        v_bit = custom_v_bitrate if custom_v_bitrate else config["v_bit"]
    a_bit = custom_a_bitrate if custom_a_bitrate else "128k"
    fps = custom_fps if custom_fps else "25"
    video_filters = f"fps={fps},scale={final_w}:{final_h},setsar=1,format=yuv420p"
    encoding_params = [
        "-c:v", "libx264",
        "-b:v", v_bit,
        "-preset", "veryfast",
        "-c:a", "aac",
        "-b:a", a_bit
    ]
    return video_filters, encoding_params