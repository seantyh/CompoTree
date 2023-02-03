from pathlib import Path
from tqdm.auto import tqdm
from .ortho_node import OrthoNode

def load_idsmap(ids_path=None):
    if not ids_path:
        ids_path = Path(__file__).parent / "data/ids.txt"

    fin = open(ids_path, "r", encoding="UTF-8")
    ids_map = {}
    for ln_i, ln in enumerate(fin):  
        if ln.startswith("#"): continue
        parts = ln.strip().split("\t")
        if len(parts) < 3:
            print("line", ln_i, ": invalid format")
        code = parts[0]
        ch = parts[1]
        try:
            components = [OrthoNode.parse(ch, x) for x in parts[2:]]
            ids_map[ch] = components
        except Exception as ex:
            print("parse error on line ", ln_i, ln) 
            import traceback as tb
            tb.print_exc()
            break
    fin.close()
    
    return ids_map