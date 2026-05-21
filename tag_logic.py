import base64
import os
import re
import config as config
def get_system_tag():
    return f"({base64.b64decode('U0dBTQ==').decode('utf-8')})"
def ensure_safe_filename(name):
    replace_map = {
        '|': '│',  
        '*': '＊',
        '<': '«',
        '>': '»',
        ':': '：',
        '"': '＂',
        '/': '／',
        '\\': '＼',
        '?': '？'
    }
    for illegal, safe in replace_map.items():
        name = name.replace(illegal, safe)
    return name
def structure_smart_filename(clean_name, user_suffix, quality_tag, extension, is_folder=False, do_clean=True, op_tag=""):
    from config import MAIN_SEPARATOR, NAME_SEPARATOR, INCLUDE_USER_SUFFIX, INCLUDE_QUALITY_IN_NAME
    if is_folder:
        return ensure_safe_filename(clean_name.strip())
    mandatory_tag = get_system_tag() 
    base_name = clean_name
    potential_separators = [MAIN_SEPARATOR, " | ", "|", " │ "]
    base_name = re.sub(r'[\(\[\s_]*' + re.escape(mandatory_tag.strip('()')) + r'[\)\]\s_]*', '', base_name, flags=re.IGNORECASE)
    if do_clean:
        for sep in potential_separators:
            if sep in base_name:
                base_name = base_name.split(sep)[0]
    base_name = base_name.strip()
    tags = []
    if INCLUDE_USER_SUFFIX and user_suffix:
        u_suffix = user_suffix.strip()
        if u_suffix.lower() not in base_name.lower():
            tags.append(u_suffix)
    tags.append(mandatory_tag)
    if INCLUDE_QUALITY_IN_NAME and quality_tag:
        q_val = str(quality_tag).lower()
        if q_val != 'original' and q_val not in base_name.lower():
            tags.append(q_val)
    if op_tag:
        op_val = str(op_tag).upper().strip()
        if op_val not in base_name.upper():
            tags.append(op_val)
    final_tags = []
    for t in tags:
        if t not in final_tags: final_tags.append(t)
    suffixes_block = NAME_SEPARATOR.join(final_tags)
    final_name = f"{base_name}{MAIN_SEPARATOR}{suffixes_block}{extension}"
    return ensure_safe_filename(final_name)
def clean_quality_redundancy(name, quality):
    if not name: return name
    patterns = [
        r'\d{3,4}p',
        r'HD',
        r'Full[ _]?HD',
    ]
    if quality:
        patterns.append(re.escape(str(quality)))
    clean_name = name
    for p in patterns:
        regex = rf'[ _\-\.\[\(]*{p}[\]\)]*'
        clean_name = re.sub(regex, '', clean_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'\s+', ' ', clean_name)
    clean_name = re.sub(r'[_ \-\.]{2,}', '_', clean_name)
    return clean_name.strip(' _-.')