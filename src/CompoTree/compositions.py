from typing import Iterable, List, Tuple
from .compo_tree import ComponentTree
from .ts_variants import TSVariants
from .char_lexicon import CharLexicon
Character = str
TradChar = Character; SimpChar = Character
Component = str
TradCompon = Component; SimpCompon = Component
Composition = Tuple[SimpChar, SimpCompon, TradChar, TradCompon]

is_simp_decomposable = lambda x: x[0] is not None and x[1] is None
is_trad_decomposable = lambda x: x[2] is not None and x[3] is None
is_simp_to_convert = lambda x: x[0] is not None and x[2] is None
is_trad_to_convert = lambda x: x[2] is not None and x[0] is None
is_simp_composable = lambda x: x[1] is not None and x[0] is None
is_trad_composable = lambda x: x[2] is not None and x[3] is None
is_trad_to_cconvert = lambda x: (x[2] is not None and x[3] is not None 
                                 and x[0] is None and x[1] is None)
is_simp_to_cconvert = lambda x: (x[0] is not None and x[1] is not None 
                                 and x[2] is None and x[3] is None)
    

class CharComposition:
    def __init__(self, items: Iterable[Composition]):
        self.items = set(items)
        self.ctree = ComponentTree.load()
        self.tsvars = TSVariants.load()
        self.lexicon = CharLexicon.load()
    
    def add(self, simpChar=None, simpCompon=None,
            tradChar=None, tradCompon=None):
        if all([x is None for x in 
                (simpChar, simpCompon, tradChar, tradCompon)]):
            raise ValueError("one of the arguments must not be None")
        pass

    def __call_func(self, func, *args):
        new_items = set()
        for item_x in self.items:
            new_x = func(item_x, *args)
            new_items.add(new_x)
        self.items = new_items

    def decompose(self):
        def __decompose(item):                            
            return item
        self.__call_func(__decompose)

    def compose(self):
        def __compose(item):
            return item
        self.__call_func(__compose)

    def char_convert(self):
        def __char_convert(item):
            return item
        self.__call_func(__char_convert)

    def compon_convert(self, constraint="position"):
        def __compon_convert(item, constraint):
            return item
        self.__call_func(__compon_convert, constraint)
    
