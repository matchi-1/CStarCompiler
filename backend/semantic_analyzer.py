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
        sym_content = {
            "value": value,
            'dtype': dtype,
            'priv': priv,
            'const': const
        }
        self.syms[sym_name] = sym_content

class SemanticAnalyzer:
    numtypes = ['int', 'long', 'float', 'double']
    def __init__(self):
        self.curr_scope = SymbolTable()
        self.errors = []

    def enter_scope(self, nodeName):
        print(F'(semantic)(dbg) ENTERING scope {nodeName}')
        self.curr_scope = SymbolTable(self.curr_scope)
    
    def exit_scope(self, nodeName):
        print(F'(semantic)(dbg) EXITING scope {nodeName}, table: {self.curr_scope.syms}')
        self.curr_scope = self.curr_scope.parent

    def visit_node(self, node):
        nodeName = type(node).__name__
        visit_func = getattr(self, f'visit_{nodeName}', None)  # Get the appropriate visit function, or None if it doesn't exist

        if visit_func is None:
            print(f"(semantic)(dbg) Not implemented yet!!!!!!!!!!!!!!!!!! node name: {nodeName}")
        else:
            print(f'(semantic)(dbg) VISITING {nodeName}!!')
            return visit_func(node)
    
    def interpret(self, node):
        self.visit_node(node)
        #print('(semantic)(dbg) global table: ', self.curr_scope.syms)
        print('(semantic)(dbg) SEMANTIC ANALYSIS DONE, NO ERRORS FOUND.')



    # ------------------------------------ NODE VISITATION FUNCS----------------------------------
    # FORMAT: visit_{node_name}
    # VALUE nodes always return tuple of dtype and value
    
    #program PLACEHODLER
    def visit_program_node(self, node):
        #PLACEHOLDER! the real thing would iterate through      
        #self.visit_node(node.program_structure_stmts[2])

        for statement in node.program_structure_stmts:
            self.visit_node(statement)
    
    #body PLACEHOLDER
    def visit_node_body(self, node):
        self.enter_scope(type(node).__name__)
        # PLACEHOLDER! idk if it's correct
        self.visit_node(node.body_codeblock_n)
        self.exit_scope(type(node).__name__)

    #code_block PLACEHODLER
    def visit_node_code_block(self, node):
        # PLACEHODLER!! idk if correct
        for statement in node.code_block_statement_n:
            self.visit_node(statement)


    def visit_node_num(self, node):
        val = 0
        if node.dtype in ['int', 'long']:
            val = int(node.val_t["tokenName"])
        elif node.dtype in ['float', 'double']:
            val = float(node.val_t["tokenName"])
        return (node.dtype, val) 
    
    def visit_node_str(self, node):
        return (node.dtype, node.val_t["tokenName"][1:-1])
    
    def visit_node_bool(self, node):
        return (node.dtype, node.val_t["tokenName"]=="true")
    
    def visit_node_iden(self, node):
        iden_symbol = self.curr_scope.get(node.id_t["tokenName"])
        if not iden_symbol:
            raise SyntaxError(f"SEMANTIC ERROR: Symbol '{node.id_t["tokenName"]}' hasnt been declared yet.")
        else:
            dtype = iden_symbol["dtype"]
            val = 0
            if dtype in ['int', 'long']:
                val = int(iden_symbol["value"])
            elif dtype in ['float', 'double']:
                val = float(iden_symbol["value"])
            return (dtype, val)
    #cont...

    #var_dec
    def visit_node_vardec(self, node):
        if self.curr_scope.get(node.id_n.id_t["tokenName"]):
            print('(semantic)(dbg) ERROR: Duplciate Symboll')
        const = node.const_b
        dtype = node.dtype_t["tokenName"]
        id = node.id_n.id_t["tokenName"]
        val_type = None
        value = None
        idec_rec = None
        if (node.vardec_cont_n):
            val_type, value = self.visit_node(node.vardec_cont_n.value_n)
            idec_rec = node.vardec_cont_n.idec_rec_n
                    
        if value and dtype != val_type:
            print('semantic)(dbg) ERROR: type mismatch')
        
        self.curr_scope.set(id, value, dtype=dtype, const=const)
        for dec_node in idec_rec or []:
            self.curr_scope.set(dec_node.id_n.id_t["tokenName"], self.visit_node(dec_node.value_n) if dec_node.value_n else None, dtype=dtype, const=const)

    # binary and unary operations
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
                if left_type == 'string':
                    if right_type != 'string':
                        print('(semantic)(dbg) ERROR: string exp only strings')
                    else:
                        return ('string', left_val + right_val)
                elif left_type in self.numtypes and right_type in self.numtypes:
                    return (dtype, left_val + right_val)
                else:
                     print('(semantic)(dbg) ERROR: only numerics')

            case '-':
                if left_type in self.numtypes and right_type in self.numtypes:
                    return (dtype, left_val - right_val)
                else:
                    print('(semantic)(dbg) ERROR: only numerics')
            case '/':
                if right_val == 0:
                    print("(semantic)(dbg) ERROR: DIVIDE BY 0")
                if left_type in self.numtypes and right_type in self.numtypes:
                    return (dtype, left_val / right_val)
                else:
                    print('(semantic)(dbg) ERROR: only numerics')
            case '*':
                if left_type in self.numtypes and right_type in self.numtypes:
                    return (dtype, left_val * right_val)
                else:
                    print('(semantic)(dbg) ERROR: only numerics')
            case '%':
                if dtype in ['float', 'double']:
                    print('(semantic)(dbg) ERROR : MODULO FLOATING POINT')
                else:
                    if left_type in self.numtypes and right_type in self.numtypes:
                        return (dtype, left_val % right_val)
                    else:
                        print('(semantic)(dbg) ERROR: only numerics')

            #relational
            case '==':
                if left_type in self.numtypes:
                    if right_type not in self.numtypes:
                        print('(semantic)(dbg) ERROR: comparison with numeric can only be with another numeric')
                elif left_type == 'string':
                    if right_type != 'string':
                        print('(semantic)(dbg) ERROR: comparisong with string can only be with another string')
                elif left_type == 'boolean':
                    if right_type != 'boolean':
                        print('(semantic)(dbg) ERROR: comparisong with boolean can only be with another boolean')
                return ('boolean', left_val == right_val)
            
            case '!=':
                if left_type in self.numtypes:
                    if right_type not in self.numtypes:
                        print('(semantic)(dbg) ERROR: comparison with numeric can only be with another numeric')
                elif left_type == 'string':
                    if right_type != 'string':
                        print('(semantic)(dbg) ERROR: comparisong with string can only be with another string')
                elif left_type == 'boolean':
                    if right_type != 'boolean':
                        print('(semantic)(dbg) ERROR: comparisong with boolean can only be with another boolean')
                return ('boolean', left_val != right_val)
            
            case '<':
                if left_type not in self.numtypes or right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                return ('boolean', left_val < right_val)  
            case '<=':
                if left_type not in self.numtypes or right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                return ('boolean', left_val <= right_val)  
            case '>':
                if left_type not in self.numtypes or right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                return ('boolean', left_val > right_val)  
            case '>=':
                if left_type not in self.numtypes or right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                return ('boolean', left_val >= right_val)  
            
            #logical
            case '&&':
                if left_type != 'boolean' or right_type != 'boolean':
                    print('(semantic)(dbg) ERROR: booleans only!!')

                return ('boolean', left_val and right_val)
            case '||':
                if left_type != 'boolean' or right_type != 'boolean':
                    print('(semantic)(dbg) ERROR: booleans only!!')

                return ('boolean', left_val or right_val)

    #unary ops
    def visit_node_un_op(self, node):
        right_type, right_val = self.visit_node(node.id_right_n)
        match node.left_t["tokenName"]:
            case '!':
                if right_type != 'boolean':
                    print('(semantic)(dbg) ERROR: only boolean')
                return ('boolean', not right_val)
            case '-':
                if right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: invalid data type')
                return (right_type, -right_val)
            case '++':
                if right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: invalid data type')
                self.curr_scope[node.id_right_n.id_n.id_t["tokenName"]] += 1
                return (right_type, right_val + 1)
            case '--':
                if right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: invalid data type')
                self.curr_scope[node.id_right_n.id_n.id_t["tokenName"]] -= 1
                return (right_type, right_val - 1 )
        if node.left_t["tokenName"] in ["bool", "string", "int", "long", "double", "float"]:
            print('(semantic)(dbg) casting')

    def visit_node_loop_stmt(self, node):
        node_loop = node.loop_stmt_n
        loop_name = type(node_loop).__name__

        self.enter_scope(loop_name)
        if loop_name == 'node_forloop':
            
            self.visit_node_vardec(node_loop.init_arg_n)
            print(f"FOUND CONDITION: {self.visit_node(node_loop.condition_n.condition_n)}")
            self.visit_node(node_loop.inc_arg_n) 
            self.visit_node(node_loop.ctrl_stmt_body_n)

        elif loop_name == 'node_while' or loop_name == 'node_do':
            print(f"FOUND CONDITION: {self.visit_node(node_loop.condition_n.condition_n)}")
            self.visit_node(node_loop.ctrl_stmt_body_n)

        elif loop_name == 'node_repeat':
            print(f"FOUND REPEAT VALUE: {self.visit_node(node_loop.repeat_value_n)}")
            self.visit_node(node_loop.ctrl_stmt_body_n)
            



        self.exit_scope(loop_name)

    #input
    # def visit_node_input(self, node):
    #     expected_dtype = node.type.t["tokenName"]
    #     prompt_n = node.prompt_n
    #     count_n = node.count_n

    #     promp_text = ""
    #     if prompt_n:
    #         _, promp_text = self.visit_node(prompt_n)

    #     user_input = input(promp_text)

    #     try:
    #         if expected_dtype == 'int':
    #             value = int(user_input) 
    #         elif expected_dtype == 'long':
    #             value = int(user_input)
    #         elif expected_dtype == 'float':
    #             value = float(user_input)
    #         elif expected_dtype == 'double':
    #             value = float(user_input)
    #         elif expected_dtype == 'string':
    #             value = user_input
    #         elif expected_dtype == 'bool':
    #             value = user_input.lower() == 'true'
    #         else:
    #             print("(semantic)(dbg) ERROR: Unsupported data type for input")
    #             return None
    #     except ValueError:
    #         print("(semantic)(dbg) ERROR: Input does not match expected data type")
    #         return None
        
    #     if count_n:
    #        _, count = self.visit_node(count_n) 
    #        if not isinstance(count, int) or count <= 0:
    #            print("(semantic)(dbg) ERROR: Invalid count for input")
    #            return None
           
    #     return (expected_dtype, value)
    
    # def visit_node_output(self, node):
    #     print_stmts_n = node.print_stmts_n
    #     print_params_n = node.print_params_n

    #     output_values = []
    #     for param in print_params_n:
    #         _, value = self.visit_node(param)
    #         output_values.append(str(value))

    #     output_text = " ".join(output_values)

    #     if print_stmts_n == "println":
    #         print(output_text)
    #     else:
    #         print(output_text, end='')
 
    #     return None

    
    #code block
    # def visit_code_block(self, node, isVoid=False):
    #     statements_n = node.code_block_statement_n  
    #     self.enter_scope()

    #     for stmt in statements_n:
    #         if isinstance(stmt, str):  
    #             self.visit_ctrl_stmt(stmt)
    #         elif isinstance(stmt, node_iden): 
    #             self.visit_var_decl(stmt)
    #         elif isinstance(stmt, node_pre_un_op):  
    #             self.visit_pre_un_op(stmt)
    #         elif isinstance(stmt, node_output):  
    #             self.visit_output(stmt)
    #         elif isinstance(stmt, node_conditional_stmt):  
    #             self.visit_conditional_stmt(stmt)
    #         elif isinstance(stmt, node_loop_stmt): 
    #             self.visit_loop_stmt(stmt)
    #         elif isinstance(stmt, node_code_block):  
    #             self.visit_code_block(stmt, isVoid)
    #         else:
    #             print("(semantic)(dbg) ERROR: Unrecognized statement type inside code block.")
        
    #     self.exit_scope()