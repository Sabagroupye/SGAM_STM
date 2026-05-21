import os
def apply_freeze_logic(v_label, intervals, fps=25):
    filters = []
    current_v = v_label
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    for i, (start, end) in enumerate(sorted_intervals):
        dur = end - start
        if dur <= 0: continue
        loop_frames = int(dur * fps)
        out_v = f"frz{i}"
        filters.append(f"{current_v}split=2[m_{i}][s_{i}];"
                       f"[s_{i}]trim=start={start}:end={start+0.05},loop=loop={loop_frames}:size=1:start=0,setpts=PTS-STARTPTS+{start}/TB[v_{i}];"
                       f"[m_{i}][v_{i}]overlay=enable='between(t,{start},{end})':eof_action=pass[{out_v}]")
        current_v = f"[{out_v}]"
    return ";".join(filters), current_v
def apply_blur_logic(v_label, intervals, strength="25:10"):
    blur_parts = []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    for s, e in sorted_intervals:
        blur_parts.append(f"boxblur={strength}:enable='between(t,{s},{e})'")
    full_blur = f"{v_label}" + ",".join(blur_parts) + "[v_blurred]"
    return full_blur, "[v_blurred]"
def apply_cut_logic(v_label, a_label, intervals, total_duration, has_audio=True, keep_only=False, seek_offset=0):
    segments = []
    if keep_only:
        segments = sorted([(max(0, s - seek_offset), max(0, e - seek_offset)) for s, e in intervals], key=lambda x: x[0])
    else:
        last_end = 0.0
        for start, end in sorted(intervals, key=lambda x: x[0]):
            if start > last_end: segments.append((last_end, start))
            last_end = end
        if last_end < total_duration: segments.append((last_end, total_duration))
    if not segments: return "", v_label, a_label
    n = len(segments)
    fs = []
    v_in = f"v_split"
    fs.append(f"{v_label}split={n}" + "".join([f"[{v_in}{i}]" for i in range(n)]))
    if has_audio and a_label:
        a_in = f"a_split"
        fs.append(f"{a_label}asplit={n}" + "".join([f"[{a_in}{i}]" for i in range(n)]))
    for i, (s, e) in enumerate(segments):
        fs.append(f"[{v_in}{i}]trim=start={s}:end={e},setpts=PTS-STARTPTS[v{i}]")
        if has_audio and a_label:
            fs.append(f"[{a_in}{i}]atrim=start={s}:end={e},asetpts=PTS-STARTPTS[a{i}]")
    v_concat = "".join([f"[v{i}]" for i in range(n)])
    fs.append(f"{v_concat}concat=n={n}:v=1:a=0[v_cut]")
    out_a = a_label
    if has_audio and a_label:
        a_concat = "".join([f"[a{i}]" for i in range(n)])
        fs.append(f"{a_concat}concat=n={n}:v=0:a=1[a_cut]")
        out_a = "[a_cut]"
    return ";".join(fs), "[v_cut]", out_a
def get_mute_filters(intervals):
    if not intervals: return None
    return ",".join([f"volume=enable='between(t,{s},{e})':volume=0" for s, e in intervals])