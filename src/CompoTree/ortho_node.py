from itertools import chain

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

    def leaf_components(self, use_flag="first"): 
        leaves = []
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
        if use_flag == "first":
            variants = chlist[0]
        elif use_flag == "all":
            variants = list(chain.from_iterable(chlist))
        else:
            variants = [x for x in chlist if use_flag in x.flag]
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
