from pathlib import Path

def load_radical_map(radical_path):
    radical_map = {}
    with radical_path.open('r', encoding="UTF-8") as fin:
        for ln in fin:
            if ln.startswith("#") or not ln.strip():
                continue
            tokens = [x.strip() for x in ln.strip().split(";")]
            radical_map[tokens[0]] = chr(int(tokens[2], 16))
    return radical_map

def load_irg_RSUnicode(irg_path, radical_map):    
    rs_index = {}
    with irg_path.open("r", encoding="UTF-8") as fin:
        for ln in fin:
            if ln.startswith("#"):
                continue
            if "kRSUnicode" not in ln:
                continue
            tokens = ln.strip().split("\t")
            ucode = tokens[0][2:]
            # if there are multiple radical entries, use the first
            rsvalue = tokens[2].split()[0].split(".") 
            rsvalue = (radical_map.get(rsvalue[0], ""), 
                    int(rsvalue[1]))
            uchr = chr(int(ucode, 16))
            rs_index[uchr] = rsvalue
    return rs_index

class Radicals:
    def __init__(self, radical_map, rs_index):
        self.radical_map = radical_map
        self.rs_index = rs_index

    @classmethod
    def load(cls, data_dir=None):
        if not data_dir:
            data_dir = Path(__file__).parent / "../../data"
        radical_path = data_dir / "CJKRadicals.txt"
        irg_path = data_dir / "Unihan_IRGSOurces_kRSUnicode.txt"
        radical_map = load_radical_map(radical_path)
        rs_index = load_irg_RSUnicode(irg_path, radical_map)
        radicals = Radicals(radical_map, rs_index)

        return radicals
    
    def query(self, ch):
        return self.rs_index.get(ch, ("", 0))
