from pathlib import Path
import re
import pickle

class CharLexicon:
    def __init__(self, lexicon):
        self.lexicon = lexicon

    def __contains__(self, x):
        return x in self.lexicon

    def __getitem__(self, x):
        return self.lexicon[x]

    def __len__(self):
        return len(self.lexicon)
        
    @classmethod
    def load(cls, path=None, topn=5000):
        data_dir = Path(__file__).parent / "../../data"        
        with (data_dir/"asbc5_characters.pkl").open("rb") as fin:
            lexicon = pickle.load(fin)
        freq_chars = sorted(lexicon.keys(), key=lexicon.get, reverse=True)
        freq_chars = filter(lambda x: re.match("[\u4e00-\u9fff]", x), freq_chars)
        lexicon = {ch: lexicon[ch] for ch in list(freq_chars)[:topn]}
        return CharLexicon(lexicon)    