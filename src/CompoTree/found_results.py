
from CompoTree.ts_variants import TSVariants


class CTFounds:
    def __init__(self, hits_list):
        self.results = hits_list
        self.tsvars = None

    def __repr__(self):
        return f"<CTFounds: {len(self.results)} entries>"

    def filter(self, idc="", pos="", flag=""):
        res = [x for x in self.results
               if x[1][-1].match(idc, pos, flag)]
        return CTFounds(res)
    
    def filter_with_lexicon(self, lexicon):
        res = [x for x in self.results
               if x[0] in lexicon]
        return CTFounds(res)

    def simplified_only(self):
        if not self.tsvars:
            self.tsvars = TSVariants.load()
        
        res = [x for x in self.results
               if self.tsvars.is_simplified(x[0])]
        return CTFounds(res)
    
    def traditional_only(self):
        if not self.tsvars:
            self.tsvars = TSVariants.load()
        res = [x for x in self.results
               if not self.tsvars.is_simplified(x[0])]
        return CTFounds(res)
    
    def tolist(self):
        return self.results