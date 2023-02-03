from itertools import chain
from typing import List
from .struct_cursor import StructureCursor

class OrthoNode:
    def __init__(self, idc, children):
        self.glyph = ""
        self.idc = idc
        self.children = children    
        self.flag = ""
    
    def __repr__(self):
        return "<{}:{}{}>".format(
                self.idc, 
                "".join(str(x) for x in self.children),
                f"({self.flag})" if self.flag else ""
        )

    def __str__(self):        
        return "{}{}{}".format(
                self.idc, 
                "".join(str(x) for x in self.children),
                f"({self.flag})" if self.flag else ""
        )
    
    def __eq__(self, other):
        if not isinstance(other, OrthoNode):
            return False
        return self.glyph == other.glyph and \
               self.idc == other.idc and \
               self.children == other.children and \
               self.flag == other.flag

    def __hash__(self):
        return hash(str(self))

    def __getitem__(self, idx_list:List[StructureCursor]):
        if not isinstance(idx_list, list):
            idx_list = [idx_list]

        if len(idx_list) > 1:
            idx = idx_list[0]
            compo = self[idx]
            if isinstance(compo, list) and len(compo) == 1:
                compo = compo[0]

            if isinstance(compo, OrthoNode):
                return compo[idx_list[1:]]
            else:
                return compo
        else:
            idx = idx_list[0]
            if not isinstance(idx, StructureCursor):                
                raise IndexError("Expect StructureCursor as index")
                        
            if self.flag and idx.flag not in self.flag:
                return None

            if idx.idc == self.idc:
                if idx.pos >= len(self.children):
                    raise IndexError("structure cursor's position is out of bound")
                rets = self.children[idx.pos]
                if isinstance(rets, list) and len(rets) == 1:
                    return rets[0]

            else:
                raise IndexError("IDC does not match")

    def print_tree(self, depth=0):    
        if self.flag:
            flag_str = f"({self.flag})"
        else:
            flag_str = ""

        glyph_str = f"({self.glyph})" if self.glyph else "(--)"
        indent = '..'*depth
        print(f"{indent}|{glyph_str}: {self.idc}{flag_str}")

        for ch_vars in self.children:
            for ch_x in ch_vars:                  
                if isinstance(ch_x, OrthoNode):
                    ch_x.print_tree(depth+1)
                else:
                    indent = '..'*(depth+1)
                    print(f"{indent}| {ch_x}")

    def depth(self):        
        depth_list = []
        for child in chain.from_iterable(self.children):
            if isinstance(child, OrthoNode):
                dval = child.depth()
            else:
                dval = 0
            depth_list.append(dval)

        if depth_list:
            return max(depth_list)+1
        else:
            return 1

    def get_component(self, idx, use_flag="first"):
        chlist = self.children[idx]
        return self.get_variants(chlist, use_flag)

    def components(self, use_flag="first"):
        return [self.get_variants(x, use_flag)
                for x in self.children]

    def leaf_components(self, use_flag="first"): 
        leaves = []
        if use_flag == "all":
            raise ValueError("all flag is not supported in leaf_components()")
        child_variants = [
                    self.get_variants(x, use_flag)
                    for x in self.children]

        for child in child_variants:            
            if isinstance(child, OrthoNode):
                compos = child.leaf_components()
                leaves.extend(compos)
            else:
                leaves.append(child)
            
        return leaves
        
    def get_variants(self, chlist, use_flag):
        # if chlist is not a list, there is no variant.
        if not isinstance(chlist, list):
            return chlist        
        
        if use_flag == "first":            
            variants = chlist[0]
        elif use_flag == "all":
            variants = chlist
        elif use_flag == "shortest":
            variants = sorted(chlist, 
                key=lambda x: 1 if isinstance(x, str) 
                                else len(x.leaf_components()), 
                reverse=False)[:1]
        elif use_flag == "longest":
            variants = sorted(chlist, 
                key=lambda x: 1 if isinstance(x, str) 
                                else len(x.leaf_components()), 
                reverse=True)[:1]
        else:
            variants = [x for x in chlist if (not x.flag) or use_flag in x.flag]
                
        if isinstance(variants, list) and len(variants) == 1:
            variants = variants[0]

        return variants

    @classmethod
    def parse(cls, glyph, intext):
        idcs = [chr(x) for x in range(0x2ff0, 0x2ffc)]
        idcs_narg = [2,2,3,3,2,2,2,2,2,2,2,2]

        if intext[0] not in idcs:
            return OrthoNode("", list(intext))
        cursor = 0    
        flag_parts = intext.split("[")
        if len(flag_parts) > 1:
            flag = flag_parts[1][:-1]
        else:
            flag = ""
        intext = flag_parts[0]    
        state = []
        
        for ch in intext:      
            if ch in idcs:
                state.append([ch, idcs_narg[idcs.index(ch)]])              
            else:
                state[-1].append(ch)
            
            # print(state)
            # check state[-1]
            last_state = state[-1]
            while len(last_state) == last_state[1]+2:            
                node = OrthoNode(last_state[0], last_state[2:])
                state.pop()
                if len(state) > 0:
                    state[-1].append(node)
                    last_state = state[-1]
                else:
                    state = [node]  
                    break           
                # print(state)             
        state[0].flag = flag
        state[0].glyph = glyph
        return state[0]
