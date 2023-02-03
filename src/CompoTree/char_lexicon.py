from pathlib import Path
import re
import pickle
from .ts_variants import TSVariants

class CharLexicon:
    def __init__(self, lexicon, trads=[], simps=[]):
        self.lexicon = set(lexicon)
        self.trads = trads
        self.simps = simps

    def __contains__(self, x):
        return x in self.lexicon

    def __iter__(self):
        return iter(self.lexicon)

    def __len__(self):
        return len(self.lexicon)
    
    @property
    def traditional(self):
        return self.trads

    @property
    def simplified(self):
        return self.simps

    @classmethod
    def load(cls, path=None, topn=5000):
        data_dir = Path(__file__).parent / "data"        
        with (data_dir/"asbc5_characters.pkl").open("rb") as fin:
            lexicon = pickle.load(fin)
        freq_chars = sorted(lexicon.keys(), key=lexicon.get, reverse=True)
        freq_chars = filter(lambda x: re.match("[\u4e00-\u9fff]", x), freq_chars)
        lexicon = {ch: lexicon[ch] for ch in list(freq_chars)[:topn]}
        trads = lexicon.copy()
        tsvars = TSVariants.load()
        simp_chars = [tsvars.convert(x)[0] for x in lexicon.keys()]
        simps = {ch: 1 for ch in simp_chars}
        for simp_x in simp_chars:
            if simp_x not in lexicon:
                lexicon[simp_x] = 1
        return CharLexicon(lexicon, trads, simps)