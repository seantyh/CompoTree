import re
from itertools import chain
from typing import List
from copy import deepcopy
from .struct_cursor import StructureCursor
from .ortho_node import OrthoNode
from .load_data import load_idsmap

class ComponentTree:
    def __init__(self, ids_map):
        self.ids_map = ids_map
        self.rev_map = {}
        for charac, nodes in self.ids_map.items():
            for dc in chain.from_iterable(x.children for x in nodes):
                # TODO: components nested deeper than the second level will not be indexed
                self.rev_map.setdefault(dc, set()).add(charac)
        
    @classmethod
    def load(cls, ids_path=None):
        idsmap = load_idsmap(ids_path)        
        ctree = ComponentTree(idsmap)
        return ctree

    def select(self, ch, cursors:List[StructureCursor], use_flag="first", return_one=True):        
        nodes = self.query(ch, use_flag=use_flag, max_depth=len(cursors))                
        if nodes:            
            ret = [x[cursors] for x in nodes]
            ret = [x for x in ret if x]
            return ret[0] if return_one and ret else ret
        else:
            return ""

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

    def filter_flag(self, nodes: List[OrthoNode], use_flag="first"):
        if use_flag == "first":
            nodes = nodes[:1]
        elif use_flag == "all":
            pass
        elif use_flag == "shortest":                      
            nodes = sorted(nodes, 
                    key=lambda x: len(x.leaf_components()), 
                    reverse=False)[:1]
        elif use_flag == "longest":
            nodes = sorted(nodes, 
                    key=lambda x: len(x.leaf_components()), 
                    reverse=True)[:1]
        else:
            nodes = [nd for nd in nodes if (not nd.flag or use_flag in nd.flag)]
        return nodes

    def query(self, in_x, use_flag="first", max_depth=-1, depth=0, filter_node=True):        
        if max_depth >= 0 and depth >= max_depth:
            return [in_x]

        if isinstance(in_x, str):      
            nodes = self.ids_map.get(in_x, None)
            nodes = self.filter_flag(nodes, use_flag)
        else:
            nodes = [in_x]
    
        
        if nodes:      
            ret_nodes = []
            for node_x in nodes:                
                if self.is_valid_node(node_x) or not filter_node:                      
                    node_y = deepcopy(node_x)                   
                    node_y.children = [self.query(x, use_flag, depth+1, max_depth) 
                                       for x in node_y.children]                    
                    ret_nodes.append(node_y)
            if ret_nodes:
                return ret_nodes
            else:
                return [in_x]
        else:
            return [in_x]
    
    def find(self, compo, max_depth=-1, depth=0, use_flag="first", bmp_only=True):
        hits = []
        bmp_pat = re.compile("[〇一-\u9fff㐀-\u4dbf豈-\ufaff]")
        characs = self.rev_map.get(compo, [])    
        for char_x in characs:
            if bmp_only and not bmp_pat.match(char_x):
                continue

            nodes = self.ids_map[char_x]
            nodes = self.filter_flag(nodes, use_flag)

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
