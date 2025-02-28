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
        val = 0
        if node.dtype in ['int', 'long']:
            val = int(node.val_t["tokenName"])
        elif node.dtype in ['float', 'double']:
            val = float(node.val_t["tokenName"])
        return (node.dtype, val) 
    def visit_node_str(self, node):
        return (node.dtype, node.val_t["tokenName"])
    def visit_node_bool(self, node):
        return (node.dtype, node.val_t["tokenName"]=="true")
    def visit_node_iden(self, node):
        iden_symbol = self.curr_scope.get(node.id_t["tokenName"])
        if not iden_symbol:
            print('(semantic)(dbg) ERROR: symbol doesnt exist')
        dtype = iden_symbol["dtype"]
        val = 0
        if dtype in ['int', 'long']:
            val = int(iden_symbol["value"])
        elif dtype in ['float', 'double']:
            val = float(iden_symbol["value"])
        return (dtype, val)
    #cont...
 
    # binary and unary operations
    # NOTE: NUBMERS ONLY FOR NOW, NO STRING ETC YET
    def visit_node_bi_op(self, node):
        left_type, left_val = self.visit_node(node.left_n)
        right_type, right_val = self.visit_node(node.right_n)
        dtype = 'int'
        if (left_type == 'long' or right_type == 'long'):
            dtype = 'long'
        if (left_type == 'float' or right_type == 'float'):
            dtype = 'float'
        if (left_type == 'double' or right_type == 'double'):
            dtype = 'double'
        match node.op_t["tokenName"]:
            case '+': 
                return (dtype, left_val + right_val)
            case '-':
                return (dtype, left_val - right_val) 
            case '/':
                if right_val == 0:
                    print("(semantic)(dbg) ERROR: DIVIDE BY 0")
                return (dtype, left_val / right_val) 
            case '*':
                return (dtype, left_val * right_val) 
            case '%':
                if dtype in ['float', 'double']:
                    print('(semantic)(dbg) ERROR : MODULO FLOATING POINT')
                return (dtype, left_val % right_val) 

            #cont... (logic n rel)