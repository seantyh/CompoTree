from itertools import chain
from copy import deepcopy
from .struct_cursor import StructureCursor
from .load_data import load_idsmap

class ComponentTree:
    def __init__(self, ids_map):
        self.ids_map = ids_map
        self.rev_map = {}
        for charac, nodes in self.ids_map.items():
            for dc in chain.from_iterable(x.children for x in nodes):
                self.rev_map.setdefault(dc, set()).add(charac)
    
    @classmethod
    def load(cls, ids_path=None):
        idsmap = load_idsmap(ids_path)        
        ctree = ComponentTree(idsmap)
        return ctree

    def is_valid_node(self, node):    
        if isinstance(node, str):      
            return False
            
        if not node.idc:
            return False

        chlist = filter(lambda x: isinstance(x, str), node.children)
        for ch in chlist:
            if 0x2460 <= ord(ch) <= 0x2472:
                return False
        return True

    def query(self, in_x, use_flag="first", filter_node=True):        
        if isinstance(in_x, str):      
            nodes = self.ids_map.get(in_x, None)
            if use_flag == "first":
                nodes = nodes[:1]
            elif use_flag == "all":
                pass
            else:
                nodes = [nd for nd in nodes if use_flag in nd.flag]
        else:
            nodes = [in_x]
    
        
        if nodes:      
            ret_nodes = []
            for node_x in nodes:
                if self.is_valid_node(node_x) or not filter_node:                      
                    node_y = deepcopy(node_x)                   
                    node_y.children = [self.query(x, use_flag) for x in node_y.children]                    
                    ret_nodes.append(node_y)
            if ret_nodes:
                return ret_nodes
            else:
                return [in_x]
        else:
            return [in_x]
    
    def find(self, compo, max_depth=-1, depth=0):
        hits = []
        characs = self.rev_map.get(compo, [])    
        for char_x in characs:
            nodes = self.ids_map[char_x]
            for node_x in nodes:        
                if compo in node_x.children:
                    struct_cursor = [StructureCursor(
                                                        node_x.idc, 
                                                        node_x.children.index(compo), 
                                                        node_x.glyph, node_x.flag)]
                    if (char_x != compo) and \
                         (max_depth < 0 or depth < max_depth-1):
                        rec_hits = self.find(char_x, max_depth, depth=depth+1)  
                    else:
                        rec_hits = []
                    hits.append((char_x, struct_cursor))
                    for rec_hit_x in rec_hits:
                        rec_char = rec_hit_x[0]
                        rec_cursor = rec_hit_x[1] + struct_cursor
                        hits.append((rec_hit_x[0], rec_cursor))
        return hits
