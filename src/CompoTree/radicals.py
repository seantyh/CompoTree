from pathlib import Path
from typing import Tuple, Optional
from .sem_variants import SemanticVariants

RadicalLocation = int
RadicalComponent = Optional[str]
RadicalNorm = str

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
        self.ts_radicals = self.build_radical_variants(radical_map)
        self.semvar = None

    @classmethod
    def load(cls, data_dir=None):
        if not data_dir:
            data_dir = Path(__file__).parent / "data"
        radical_path = data_dir / "CJKRadicals.txt"
        irg_path = data_dir / "Unihan_IRGSOurces_kRSUnicode.txt"
        radical_map = load_radical_map(radical_path)
        rs_index = load_irg_RSUnicode(irg_path, radical_map)
        radicals = Radicals(radical_map, rs_index)

        return radicals
    
    def query(self, ch, norm_trad=False):
        rad = self.rs_index.get(ch, ("", 0))
        if norm_trad:
            rad = (self.ts_radicals.get(rad[0], rad[0]), rad[1])
        return rad
        
    def build_radical_variants(self, radical_map):
        rad_vars = {}
        for rid, radical in radical_map.items():
            if rid.endswith("'"):
                # it's a simplified radical
                trad_radical = radical_map[rid[:-1]]
                rad_vars[radical] = trad_radical
        return rad_vars
    
    def get_semvar_inst(self):
        if not self.semvar:
            self.semvar = SemanticVariants.load()
            self.semvar.var_map.update({
                "𧾷": ["足"],
                "阝": ["阜", "邑"],
                "王": ["玉"],
                "月": ["肉"],
                "朩": ["木"],
                "覀": ["襾"],
                "户": ["戶"],
                "宀": ["穴"],
                "匚": ["匸"],
                "罒": ["网"],

            })
        return self.semvar
    
    def locate_radical(
            self, ch, compos
            ) -> Tuple[RadicalLocation, RadicalComponent, RadicalNorm]:
        norm_radical = self.query(ch)[0]
        semvar_inst = self.get_semvar_inst()
        for compo_i, compo_x in enumerate(compos):
            vars = semvar_inst.variants(compo_x)
            if norm_radical==compo_x or norm_radical in vars:
                return compo_i, compo_x, norm_radical
        return -1, None, norm_radical