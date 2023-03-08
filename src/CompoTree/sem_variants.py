from pathlib import Path

def load_var_data(var_path):
    var_map = {}
    with var_path.open("r", encoding="UTF-8") as fin:
        for ln in fin:
            if ln.startswith("#") or not ln.strip():
                continue
            tokens = ln.strip().split("\t")
            uchar = chr(int(tokens[0][2:], 16))
            var_fields = [x.split("<")[0][2:] for x in tokens[2].split()]
            var_char = [chr(int(var_x, 16)) for var_x in var_fields]
            if tokens[1].startswith("kSemantic"):
                var_map[uchar] = var_char
    return var_map

class SemanticVariants:
    def __init__(self, var_map):
        self.var_map = var_map

    @classmethod
    def load(self, var_path=None):
        if var_path is None:
            var_path = Path(__file__).parent / "data/Unihan_Variants.txt"
        var_map = load_var_data(var_path)
        return SemanticVariants(var_map)
    
    def has_variants(self, ch):
        return ch in self.var_map

    def variants(self, ch):
        return self.var_map.get(ch, [])