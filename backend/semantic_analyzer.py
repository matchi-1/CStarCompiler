class SymbolTable:
    def __init__(self, parent=None):
        self.syms = {} #key: string val: dict
        self.parent = parent

    def get(self, sym_name):
        sym = self.syms.get(sym_name, None)
        if not sym and self.parent:
            return self.parent.get(sym_name)
        return sym
        
    
    # ALWAYS NAME ARGS FOR DTYPE PRIV AND CONST WHEN CALLING SET
    def set(self, sym_name, value, dtype=None, priv=False, const=False):
        self.syms[sym_name]["value"] = value
        self.syms[sym_name]["dtype"] = dtype
        self.syms[sym_name]["priv"] = priv
        self.syms[sym_name]["const"] = const

class SemanticAnalyzer:
    def __init__(self):
        self.curr_scope = SymbolTable()

    def enter_scope(self):
        self.curr_scope = SymbolTable(self.curr_scope)
    
    def exit_scope(self):
        self.curr_scope = self.curr_scope.parent