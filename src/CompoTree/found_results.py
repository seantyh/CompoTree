
class CTFounds:
    def __init__(self, hits_list):
        self.results = hits_list

    def __repr__(self):
        return f"<CTFounds: {len(self.results)} entries>"

    def filter(self, idc="", pos="", flag=""):
        return [x for x in self.results
                if x[1][-1].match(idc, pos, flag)]