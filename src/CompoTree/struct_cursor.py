
class StructureCursor:
  def __init__(self, idc, pos, glyph="", flag=""):
    self.idc = idc
    self.pos = pos
    self.glyph = glyph
    self.flag = flag

  def __repr__(self):
    flag_str = f"({self.flag})" if self.flag else ""
    glyph_str = f"({self.glyph})" if self.glyph else ""
    return "{}{}{}{}".format(self.idc, self.pos, self.glyph, flag_str)
  
  def match(self, idc="", pos="", flag=""):
    is_match = True
    if idc: is_match &= (idc==self.idc)
    if pos: is_match &= (pos==self.pos)
    if flag: is_match &= (flag in self.flag)
    return is_match