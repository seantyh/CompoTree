from pathlib import Path

def load_var_data(var_path):
    ts_map = {}
    st_map = {}
    with var_path.open("r", encoding="UTF-8") as fin:
        for ln in fin:
            if ln.startswith("#") or not ln.strip():
                continue
            tokens = ln.strip().split("\t")
            uchar = chr(int(tokens[0][2:], 16))
            var_fields = [x.split("<")[0][2:] for x in tokens[2].split()]
            var_char = [chr(int(var_x, 16)) for var_x in var_fields]
            if tokens[1].startswith("kTrad"):
                st_map[uchar] = var_char
            elif tokens[1].startswith("kSimp"):
                ts_map[uchar] = var_char
    return ts_map, st_map
        

class TSVariants:
    def __init__(self, ts_map, st_map):
        self.ts_map = ts_map
        self.st_map = st_map

    @classmethod
    def load(self, var_path=None):
        if var_path is None:
            var_path = Path(__file__).parent / "data/Unihan_Variants.txt"
        ts_map, st_map = load_var_data(var_path)
        return TSVariants(ts_map, st_map)
    
    def is_traditional(self, ch):
        return ch in self.ts_map

    def is_simplified(self, ch):
        return ch in self.st_map

    def convert(self, ch, t2s_only=False):
        if ch in self.ts_map:
            return self.ts_map[ch]
        elif not t2s_only and ch in self.st_map:
            return self.st_map[ch]
        else:
            return ch
