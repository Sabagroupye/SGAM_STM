import os
from config import *
from internal_paths import CORE_TEXTS, CORE_ASSETS_DIR
def parse_time(val):
    try:
        if isinstance(val, (int, float)): return float(val)
        p = str(val).split(':')
        if len(p) == 3: return int(p[0])*3600 + int(p[1])*60 + float(p[2])
        if len(p) == 2: return int(p[0])*60 + float(p[1])
        return float(val)
    except: return 10.0
def get_pos_coords(pos_str, w_sym="tw", h_sym="th"):
    pos_map = {
        'Top-Left': ["20", "20"],
        'Top-Center': [f"(W-{w_sym})/2", "20"],
        'Top-Right': [f"W-{w_sym}-20", "20"],
        'Middle-Left': ["20", f"(H-{h_sym})/2"],
        'Center': [f"(W-{w_sym})/2", f"(H-{h_sym})/2"],
        'Middle-Right': [f"W-{w_sym}-20", f"(H-{h_sym})/2"],
        'Bottom-Left': ["20", f"H-{h_sym}-20"],
        'Bottom-Center': [f"(W-{w_sym})/2", f"H-{h_sym}-20"],
        'Bottom-Right': [f"W-{w_sym}-20", f"H-{h_sym}-20"],
    }
    return pos_map.get(pos_str, [f"(W-{w_sym})/2", f"H-{h_sym}-20"])
def build_layer_filter(current_v, layer, i, res_h, video_dur, forced_start=None):
    if 'timing' not in layer:
        layer = {
            'type': layer.get('type', 'text'),
            'timing': {'anchor': 'Start', 'offset': layer.get('start', 0), 'duration': layer.get('dur', 10)},
            'content': {'text': layer.get('content', '')},
            'style': {
                'pos': layer.get('pos', 'Center'), 
                'size_ratio': layer.get('size_ratio', 20), 
                'color': layer.get('color', 'white'), 
                'opac': layer.get('opac', 1.0), 
                'mode': layer.get('mode', 'Overlay')
            },
            'animation': {
                'type': layer.get('move_type', 'None'), 
                'dir': layer.get('move_dir', 'In'), 
                'count': layer.get('appear_count', 1)
            }
        }
    l_type = layer.get('type', 'text')
    timing = layer.get('timing', {})
    content_data = layer.get('content', {})
    style = layer.get('style', {})
    anim = layer.get('animation', {})
    if forced_start is not None:
        start_global = forced_start
        duration = timing.get('duration', 10)
    else:
        anchor = timing.get('anchor', 'Start')
        offset = timing.get('offset', 0)
        duration = timing.get('duration', 10)
        if anchor == 'Start of Video' or anchor == 'Start':
            start_global = offset
        elif anchor == 'Middle of Video' or anchor == 'Middle':
            start_global = (video_dur / 2) + offset
        elif anchor == 'End of Video' or anchor == 'End':
            if duration == -1: duration = video_dur 
            start_global = (video_dur - duration) + offset
        else:
            start_global = offset
    if duration == -1:
        duration = max(0, video_dur - start_global)
    end_global = min(start_global + duration, video_dur)
    move_type = anim.get('type', 'None')
    move_dir = anim.get('dir', 'In')
    count = int(anim.get('count', 1))
    interval = video_dur / count if count > 0 else video_dur
    intervals = []
    for c in range(count):
        s = c * interval + start_global
        e = min(s + duration, video_dur)
        if s < video_dur:
            intervals.append(f"between(t,{s},{e})")
    enable_expr = "+".join(intervals) if intervals else "0"
    is_dt = (l_type == 'text')
    w_sym = "tw" if is_dt else "w"
    h_sym = "th" if is_dt else "h"
    px, py = get_pos_coords(style.get('pos', 'Center'), w_sym=w_sym, h_sym=h_sym)
    color = style.get('color', 'white')
    opac = float(style.get('opac', 1.0))
    ratio = float(style.get('size_ratio', 20))
    mode = style.get('mode', 'Overlay')
    if move_type != 'None':
        anim_dur = 1.0 
        if count > 1:
            t_rel = f"mod(t,{interval})"
            t_start_rel = str(start_global % interval) if count > 0 else "0"
            time_since_start = f"({t_rel}-{t_start_rel})"
            time_until_end = f"({duration}-{time_since_start})"
        else:
            time_since_start = f"(t-{start_global})"
            time_until_end = f"({end_global}-t)"
        prog_in = f"max(0,min(1,{time_since_start}/{anim_dur}))"
        prog_out = f"max(0,min(1,(({anim_dur}-{time_until_end})/{anim_dur})))"
        if move_type == 'L-R':
            if move_dir == 'In': px = f"-{w_sym} + ({px} + {w_sym})*{prog_in}"
            else: px = f"{px} + (W - {px})*{prog_out}"
        elif move_type == 'R-L':
            if move_dir == 'In': px = f"W + ({px} - W)*{prog_in}"
            else: px = f"{px} - ({px} + {w_sym})*{prog_out}"
        elif move_type == 'T-B':
            if move_dir == 'In': py = f"-{h_sym} + ({py} + {h_sym})*{prog_in}"
            else: py = f"{py} + (H - {py})*{prog_out}"
        elif move_type == 'B-T':
            if move_dir == 'In': py = f"H + ({py} - H)*{prog_in}"
            else: py = f"{py} - ({py} + {h_sym})*{prog_out}"
    if l_type == 'text':
        text_val = content_data.get('text', '').strip()
        if not text_val: return "", current_v
        temp_path = os.path.join(CORE_ASSETS_DIR, f"layer_{i}.txt")
        with open(temp_path, 'w', encoding='utf-8') as f: f.write(text_val)
        safe_font = DEFAULT_FONT_PATH.replace('\\', '/').replace(':', '\\:')
        bg_opac = "1.0" if 'Interrupt' in mode else "0.4"
        opts = [f"fontfile='{safe_font}'", f"textfile='layer_{i}.txt'", "reload=1", f"fontcolor={color}@{opac}", f"fontsize=h/{ratio}", f"x='{px}'", f"y='{py}'", f"enable='{enable_expr}'", "fix_bounds=1", "box=1", f"boxcolor=black@{bg_opac}", "boxborderw=5"]
        f_str = "drawtext=" + ":".join(opts)
        return f"{current_v}{f_str}[v_l{i}]", f"[v_l{i}]"
    return "", current_v
def apply_visual_signature(current_v, res_h, input_idx=None):
    from utils import verify_signature_image
    sig_valid = False
    sig_path = os.path.join(CORE_ASSETS_DIR, "SG_LOGTURE")
    if os.path.exists(sig_path):
        if verify_signature_image(sig_path, expected_w=3189, expected_h=1417):
            sig_valid = True
    if sig_valid and input_idx is not None:
        sig_size = 3.5 
        sig_h = int(res_h * (sig_size / 100))
        if sig_h < 5: sig_h = 5
        padding = int(res_h * (2.0 / 100))
        if padding < 8: padding = 8
        f_str = f"[{input_idx}:v]format=rgba,scale=-1:{sig_h},colorchannelmixer=aa=0.5[sig_img];"
        f_str += f"{current_v}[sig_img]overlay='W-w-{padding}':'H-h-{padding}'[v_sig]"
        return f_str, "[v_sig]"
    else:
        from metadata import get_system_tag
        tag = get_system_tag().strip('()')
        sig_file = os.path.join(CORE_ASSETS_DIR, "sig_tag.txt")
        with open(sig_file, 'w', encoding='utf-8') as f: f.write(tag)
        padding = int(res_h * 0.02)
        if padding < 10: padding = 10
        f_size = int(res_h * 0.03)
        if f_size < 12: f_size = 12
        safe_f = DEFAULT_FONT_PATH.replace('\\', '/').replace(':', '\\:')
        sig_txt = f"drawtext=fontfile='{safe_f}':textfile='sig_tag.txt':reload=1:x=W-tw-{padding}:y=H-th-{padding}:fontsize={f_size}:fontcolor=white@0.4"
        return f"{current_v}{sig_txt}[v_sig]", "[v_sig]"
def get_editor_filters(logo_pos_str, logo_size, logo_opac, res_h=720, duration=0, text_options=None, layers=None, bounce_seq=None, sig_input_idx=None):
    filters = []
    layers = layers or []
    sorted_layers = sorted(layers, key=lambda x: x.get('timing', {}).get('offset', 0))
    interrupt_shifts = []
    current_v = "[main_v]"
    v_pts_expr = "T"
    a_pts_expr = "T"
    total_added_dur = 0
    for layer in sorted_layers:
        mode = "Overlay"
        if 'Interrupt' in mode:
            l_dur = float(layer.get('timing', {}).get('duration', 10))
            if l_dur <= 0: continue
            l_offset = float(layer.get('timing', {}).get('offset', 0))
            l_anchor = layer.get('timing', {}).get('anchor', 'Start')
            l_start_orig = l_offset
            if 'Middle' in l_anchor: l_start_orig += (duration / 2)
            elif 'End' in l_anchor: l_start_orig += (duration - l_dur)
            interrupt_shifts.append({
                'start': l_start_orig, 
                'dur': l_dur, 
                'shifted_end': None
                            })
            v_pts_expr = f"if(between(T,{l_start_orig + total_added_dur},{l_start_orig + total_added_dur + l_dur}),{l_start_orig}/TB,if(gt(T,{l_start_orig + total_added_dur + l_dur}),(T-{l_dur})/TB,{v_pts_expr}))"
            a_pts_expr = f"if(between(T,{l_start_orig + total_added_dur},{l_start_orig + total_added_dur + l_dur}),{l_start_orig}/TB,if(gt(T,{l_start_orig + total_added_dur + l_dur}),(T-{l_dur})/TB,{a_pts_expr}))"
            total_added_dur += l_dur
    if interrupt_shifts:
        filters.append(f"{current_v}setpts='{v_pts_expr}'[v_warped]")
        current_v = "[v_warped]"
    final_duration = duration + total_added_dur
    for i, layer in enumerate(sorted_layers):
        l_offset = float(layer.get('timing', {}).get('offset', 0))
        l_anchor = layer.get('timing', {}).get('anchor', 'Start')
        l_dur = float(layer.get('timing', {}).get('duration', 10))
        l_start_orig = l_offset
        if 'Middle' in l_anchor: l_start_orig += (duration / 2)
        elif 'End' in l_anchor: l_start_orig += (duration - (l_dur if l_dur>0 else 0))
        shift_for_this_layer = 0
        for s in interrupt_shifts:
            if s['start'] < l_start_orig:
                shift_for_this_layer += s['dur']
        res_f, current_v = build_layer_filter(current_v, layer, i, res_h, final_duration, forced_start = l_start_orig + shift_for_this_layer)
        if res_f:
            filters.append(res_f)
    if os.path.exists(CORE_TEXTS) and BASE_TEXT_ENABLED:
        bt_shift = 0
        for s in interrupt_shifts:
            if s['start'] < BASE_TEXT_START: bt_shift += s['dur']
        safe_f = DEFAULT_FONT_PATH.replace('\\', '/').replace(':', '\\:')
        draw = f"drawtext=fontfile='{safe_f}':textfile='texts.txt':reload=1:fontcolor={BASE_TEXT_COLOR}:fontsize=h/{BASE_TEXT_SIZE_RATIO}:box=1:boxcolor=black@0.5:x=(W-tw)/2:y=(H-th)/2:fix_bounds=1:line_spacing=5:enable='between(t,{BASE_TEXT_START + bt_shift},{BASE_TEXT_START + bt_shift + BASE_TEXT_DURATION})'"
        filters.append(f"{current_v}{draw}[v_base]")
        current_v = "[v_base]"
    sig_f, current_v = apply_visual_signature(current_v, res_h, input_idx=sig_input_idx)
    filters.append(sig_f)
    calc_logo_h = int(res_h * (logo_size / 100))
    if calc_logo_h < 5: calc_logo_h = 5
    filters.append(f"[LOGO_INPUT]format=rgba,scale=-1:{calc_logo_h},colorchannelmixer=aa={logo_opac}[logo]")
    def get_pos_helper(code):
        p = {'TL':["20","20"],'TR':["W-w-20","20"],'BL':["20","H-h-20"],'BR':["W-w-20","H-h-20"],'TC':["(W-w)/2","20"],'BC':["(W-w)/2","H-h-20"],'ML':["20","(H-h)/2"],'MR':["W-w-20","(H-h)/2"],'C':["(W-w)/2","(H-h)/2"]}
        return p.get(code, ["(W-w)/2", "H-h-20"])
    raw_seq = bounce_seq or "TL,TR,BR,BL"
    seq = [s.strip() for s in raw_seq.split(',') if s.strip()]
    num = len(seq)
    wait = final_duration/num if (LOGO_BOUNCE_LINKED_TO_DURATION and final_duration>0) else parse_time(LOGO_BOUNCE_WAIT)
    mod_val = wait * num
    if logo_pos_str == 'Dynamic-Bounce' and num > 1:
        x_e, y_e = "", ""
        for i in range(num):
            coord = get_pos_helper(seq[i])
            if i == num - 1: x_e += coord[0]; y_e += coord[1]
            else:
                cond = f"between(mod(t,{mod_val}),{i*wait},{(i+1)*wait})"
                x_e += f"if({cond},{coord[0]},"; y_e += f"if({cond},{coord[1]},"
        x_e += ")"*(num-1); y_e += ")"*(num-1)
        filters.append(f"{current_v}[logo]overlay='{x_e}':'{y_e}'[final_v]")
    else:
        pos = seq[0] if (logo_pos_str == 'Dynamic-Bounce' and num > 0) else logo_pos_str
        coord = get_pos_helper(pos)
        filters.append(f"{current_v}[logo]overlay='{coord[0]}':'{coord[1]}'[final_v]")
    if not filters:
        filters.append(f"{current_v}null[final_v]")    
    return ";".join(filters), "[final_v]", {"a_pts": a_pts_expr, "shifts": interrupt_shifts}