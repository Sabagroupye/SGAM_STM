import os
import config as config
from utils import get_video_info
def assemble_audio_command(source_file, mode, card_settings, trim_data=None, apply_signature=False):
    inputs = ["ffmpeg", "-i", source_file]
    encoding_args = []
    filter_complex = []
    if trim_data:
        if trim_data.get('mode') == 'Range':
            start = trim_data.get('start', 0)
            end = trim_data.get('end', 0)
            inputs.insert(1, "-ss")
            inputs.insert(2, str(start))
            if end and str(end) != '0':
                inputs.insert(3, "-to")
                inputs.insert(4, str(end))
    from internal_paths import CORE_ASSETS_DIR
    mandatory_sig = os.path.join(CORE_ASSETS_DIR, "SG_Pr")
    remix_sig = config.AUDIO_SIGNATURE_PATH
    is_convert_mode = (mode == '2')
    input_counter = 1 
    m_idx, r_idx = -1, -1
    if not is_convert_mode:
        if os.path.exists(mandatory_sig):
            inputs.extend(["-i", mandatory_sig])
            m_idx = input_counter
            input_counter += 1
        if apply_signature and os.path.exists(remix_sig):
            inputs.extend(["-i", remix_sig])
            r_idx = input_counter
            input_counter += 1
    if not is_convert_mode and (m_idx != -1 or r_idx != -1):
        filter_complex.append(f"[0:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[main_raw]")
        if m_idx != -1:
            filter_complex.append(f"[{m_idx}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume={config.AUDIO_SIGNATURE_SIG_VOL}[m_fmt]")
        if r_idx != -1:
            filter_complex.append(f"[{r_idx}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume={config.AUDIO_SIGNATURE_SIG_VOL}[r_fmt]")
            filter_complex.append(f"[r_fmt]asplit=2[r_start_raw][r_end]")
        current_main = "[main_raw]"
        if r_idx != -1 and config.AUDIO_SIGNATURE_MODE in ["Start", "Both"]:
            r_info = get_video_info(remix_sig)
            r_dur = r_info['dur'] if r_info else 5
            filter_complex.append(f"[main_raw]volume='if(between(t,0,{r_dur}),0.3,1.0)'[main_ducked]")
            filter_complex.append(f"[main_ducked][r_start_raw]amix=inputs=2:duration=first[main_mixed]")
            current_main = "[main_mixed]"
        concat_inputs = [current_main]
        if r_idx != -1 and config.AUDIO_SIGNATURE_MODE in ["End", "Both"]:
            concat_inputs.append("[r_end]")
        if m_idx != -1:
            concat_inputs.append("[m_fmt]")
        if len(concat_inputs) > 1:
            inputs_str = "".join(concat_inputs)
            filter_complex.append(f"{inputs_str}concat=n={len(concat_inputs)}:v=0:a=1[a_final]")
            a_map = "[a_final]"
        else:
            a_map = current_main
    else:
        a_map = "0:a?"
    bitrate = card_settings.get('bitrate', config.AUDIO_QUALITY)
    if bitrate == 'Auto':
        src_info = get_video_info(source_file)
        bitrate = f"{src_info.get('bitrate', 192)}k" if src_info else "192k"
    encoding_args.extend(["-c:a", "libmp3lame", "-b:a", bitrate, "-ar", "44100", "-ac", "2"])
    return {
        'inputs': inputs,
        'filter_complex': ";".join(filter_complex),
        'map': a_map,
        'encoding_args': encoding_args
    }