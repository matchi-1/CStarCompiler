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

    def visit_node(self, node ):
        visit_func = getattr(self, f'visit_{type(node).__name__}') #get the appropriate visit func
        return visit_func(node)
    
    # ---NODE VISITATION FUNCS---
    # FORMAT: visit_{node_name}
    # VALUE nodes always return tuple of dtype and value
    def visit_node_num(self, node):
        return (node.dtype, node.val_t["tokenName"]) 
    def visit_node_str(self, node):
        return (node.dtype, node.val_t["tokenName"])
    def visit_node_bool(self, node):
        return (node.dtype, node.val_t["tokenName"])
    #cont...

    #binary and unary operations
    # def visit_node_bi_op(self, node):
    #     match node.op_t["tokenName"]:
    #         case '+':
                
    #         case '-':
                
    #         case '/':
                
    #         case '*':

    #         case '%':

    #         #cont... (logic n rel)