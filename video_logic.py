import os
import time
import config as config
from utils import get_video_info
from converter import get_converter_args
from editor import get_editor_filters
from censor import apply_freeze_logic, apply_cut_logic, apply_blur_logic
from config import BLUR_INTENSITY
from utils import COMPANY_NAME
from internal_paths import CORE_LOGO, CORE_POSTER
def assemble_video_command(video_path, mode, settings, censor_data=None):
    info = get_video_info(video_path)
    if not info: return None
    dur = info['dur']
    src_h = info['h']
    src_fps = info['fps']
    from utils import get_binary_path
    inputs = [get_binary_path("ffmpeg")]
    seek_offset = 0
    work_dur = dur
    if censor_data and mode in ['1', '3'] and censor_data["mode"] == "Cut" and censor_data.get("keep_only", False):
        ivs = censor_data.get("ivs", [])
        if len(ivs) == 1:
            start_s = ivs[0][0]
            if start_s > 2: 
                seek_offset = start_s
                inputs.extend(["-ss", str(seek_offset)])
                work_dur = ivs[0][1] - ivs[0][0]
    inputs.extend(["-i", video_path])
    idx_map = {}
    filter_complex = []
    current_v = "[0:v]"
    has_audio = info.get('has_audio', False)
    a_label = "[0:a]" if has_audio else None
    target_q = settings.get('target_q', config.DEFAULT_RESOLUTION)
    if mode != '4' and str(target_q).lower() != 'original':
        target_h = int(str(target_q).replace('p',''))
        final_h = min(src_h, target_h)
        res_f, enc_p = get_converter_args(f"{final_h}p", source_h=src_h, custom_fps=settings.get('fps', config.DEFAULT_FPS))
        filter_complex.append(f"{current_v}{res_f}[v_scaled]")
        current_v = "[v_scaled]"
    else:
        if mode == '4':
            enc_p = ["-c:v", "copy", "-c:a", "copy"]
        else:
            enc_p = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k"]
        final_h = src_h
    if censor_data and mode in ['1', '3']:
        if censor_data["mode"] == "Freeze":
            cf, cl = apply_freeze_logic(current_v, censor_data["ivs"], fps=src_fps)
            filter_complex.append(cf); current_v = cl
        elif censor_data["mode"] == "Blur":
            cf, cl = apply_blur_logic(current_v, censor_data["ivs"], strength=BLUR_INTENSITY)
            filter_complex.append(cf); current_v = cl
        elif censor_data["mode"] == "Cut":
            cf, cv, ca = apply_cut_logic(current_v, a_label, censor_data["ivs"], dur, has_audio=has_audio, keep_only=censor_data.get("keep_only", False), seek_offset=seek_offset)
            filter_complex.append(cf); current_v = cv; a_label = ca
    if mode in '12':
        logo_idx = None
        if os.path.exists(CORE_LOGO):
            inputs.extend(["-i", CORE_LOGO])
            logo_idx = inputs.count("-i") - 1
            idx_map["logo"] = logo_idx
        current_layers = settings.get('layers', [])
        from config import CORE_ASSETS_DIR
        sig_path = os.path.join(CORE_ASSETS_DIR, "SG_LOGTURE")
        sig_input_idx = None
        if os.path.exists(sig_path):
            inputs.extend(["-i", sig_path])
            sig_input_idx = inputs.count("-i") - 1
        t_opts = {
            'text': COMPANY_NAME,
            'color': settings.get('text_color','white'), 'size': settings.get('text_size',40), 
            'opac': settings.get('text_opac',0.8), 'halign': settings.get('text_h','Center'), 
            'valign': settings.get('text_v','Bottom'), 'start': settings.get('text_start',0), 
            'dur': settings.get('text_dur',10)
        } if settings.get('text_enabled') else None
        ef, next_v, extra = get_editor_filters(
            settings.get('logo_pos_str', 'Top-Right'), 
            float(settings.get('logo_size', 20)), 
            float(settings.get('logo_opac', 0.8)), 
            res_h=final_h, 
            duration=work_dur, 
            text_options=t_opts,
            layers=current_layers,
            bounce_seq=settings.get('logo_bounce_seq'),
            sig_input_idx=sig_input_idx
        )
        l_idx_str = f"[{logo_idx}:v]" if logo_idx is not None else "color=c=black@0:s=1x1[logo_empty];[logo_empty]"
        ef_resolved = ef.replace("[main_v]", current_v).replace("[LOGO_INPUT]", l_idx_str)
        filter_complex.append(ef_resolved)
        current_v = next_v
        shifts = extra.get('shifts', [])
        if extra and a_label and shifts:
            a_pts = extra.get('a_pts', 'T')
            duck_expr = "1"
            total_shift = 0
            mixed_inputs = []
            for i, s in enumerate(shifts):
                s_warped = s['start'] + total_shift
                e_warped = s_warped + s['dur']
                duck_expr = f"({duck_expr})*(1-between(t,{s_warped},{e_warped}))"
                total_shift += s['dur']
            filter_complex.append(f"{a_label}asetpts='{a_pts}',volume='{duck_expr}'[a_main_warped]")
            mixed_inputs.insert(0, "[a_main_warped]")
            if len(mixed_inputs) > 1:
                mix_str = "".join(mixed_inputs)
                filter_complex.append(f"{mix_str}amix=inputs={len(mixed_inputs)}:duration=first[a_final]")
                a_label = "[a_final]"
            else:
                a_label = "[a_main_warped]"
    elif mode in ['3', '5']:
        from config import CORE_ASSETS_DIR
        from editor import apply_visual_signature
        sig_path = os.path.join(CORE_ASSETS_DIR, "SG_LOGTURE")
        sig_input_idx = None
        if os.path.exists(sig_path):
            inputs.extend(["-i", sig_path])
            sig_input_idx = inputs.count("-i") - 1
        sig_f, current_v = apply_visual_signature(current_v, final_h, input_idx=sig_input_idx)
        filter_complex.append(sig_f)
    if mode in '1235' and os.path.exists(CORE_POSTER):
        inputs.extend(["-i", CORE_POSTER])
        poster_idx = inputs.count("-i") - 1
        idx_map["poster"] = poster_idx
    full_fc = ";".join([f for f in filter_complex if f])
    from utils import log_event
    log_event(f"Full Filter Complex: {full_fc}", level="DEBUG")
    return {
        'inputs': inputs,
        'filter_complex': full_fc,
        'video_label': current_v,
        'v_label': current_v,
        'audio_label': a_label,
        'a_label': a_label,
        'enc_p': enc_p,
        'encoding_args': enc_p,
        'idx_map': idx_map
    }